/******************************************
Copyright (c) 2016, Mate Soos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
***********************************************/

#ifndef __SEARCHER_H__
#define __SEARCHER_H__

#include <array>

#include "propengine.h"
#include "solvertypes.h"
#include "time_mem.h"
#include "hyperengine.h"
#include "simplefile.h"
#include "searchstats.h"
#include "gqueuedata.h"

#ifdef CMS_TESTING_ENABLED
#include "gtest/gtest_prod.h"
#endif


namespace CMSGen {

class Solver;
class SQLStats;
class VarReplacer;
class EGaussian;
class DistillerLong;

using std::string;
using std::cout;
using std::endl;

struct OTFClause
{
    Lit lits[3];
    unsigned size;
};

struct VariableVariance
{
    double avgDecLevelVarLT = 0;
    double avgTrailLevelVarLT= 0;
    double avgDecLevelVar = 0;
    double avgTrailLevelVar = 0;
};

class Searcher : public HyperEngine
{
    public:
        Searcher(const SolverConf* _conf, Solver* solver, std::atomic<bool>* _must_interrupt_inter);
        virtual ~Searcher();
        ///////////////////////////////
        // Solving
        //
        lbool solve(
            uint64_t max_confls
        );
        void finish_up_solve(lbool status);
        void reduce_db_if_needed();
        bool clean_clauses_if_needed();
        bool must_abort(lbool status);
        uint64_t luby_loop_num = 0;


        vector<lbool>  model;
        vector<Lit>    decisions_reaching_model; // the decisions needed to reach current model
        bool           decisions_reaching_model_valid = false;
        vector<Lit>   conflict;     ///<If problem is unsatisfiable (possibly under assumptions), this vector represent the final conflict clause expressed in the assumptions.
        template<bool update_bogoprops>
        PropBy propagate();

        ///////////////////////////////
        // Stats
        //Restart print status
        uint64_t lastRestartPrint = 0;
        uint64_t lastRestartPrintHeader = 0;
        void     print_restart_stat();
        void     print_iteration_solving_stats();
        void     print_restart_header();
        void     print_restart_stat_line() const;
        void     print_restart_stats_base() const;
        void     print_clause_stats() const;
        uint64_t sumRestarts() const;
        const SearchHist& getHistory() const;

        size_t hyper_bin_res_all(const bool check_for_set_values = true);
        std::pair<size_t, size_t> remove_useless_bins(bool except_marked = false);

        ///Returns 0 if not inside, 1 if TRUE and 2 if FALSE
        lbool var_inside_assumptions(const uint32_t var) const
        {
            #ifdef SLOW_DEBUG
            assert(var < nVars());
            #endif
            return varData[var].assumption;
        }
        lbool lit_inside_assumptions(const Lit lit) const
        {
            #ifdef SLOW_DEBUG
            assert(lit.var() < nVars());
            #endif
            if (varData[lit.var()].assumption == l_Undef) {
                return l_Undef;
            } else {
                lbool val = varData[lit.var()].assumption;
                return val ^ lit.sign();
            }
        }
        template<bool do_insert_var_order = true, bool update_bogoprops = false>
        void cancelUntil(uint32_t level, uint32_t clid_plus = 0); ///<Backtrack until a certain level.
        bool check_order_heap_sanity() const;

        void consolidate_watches(const bool full);

        //Gauss
        #ifdef USE_GAUSS
        void clear_gauss_matrices();
        enum class gauss_ret {g_cont, g_nothing, g_false};
        gauss_ret gauss_jordan_elim();
        vector<EGaussian*> gmatrices;
        vector<GaussQData> gqueuedata;

        uint32_t sum_gauss_called = 0;
        uint32_t sum_gauss_confl = 0;
        uint32_t sum_gauss_prop = 0;
        uint32_t sum_gauss_unit_truths = 0;
        uint32_t sum_gauss_entered_mtx = 0;
        uint32_t get_sum_gauss_called() const;
        uint32_t get_sum_gauss_confl() const;
        uint32_t get_sum_gauss_prop() const;
        uint32_t get_sum_gauss_unit_truths() const;
        #endif

        double get_cla_inc() const
        {
            return cla_inc;
        }

        //assumptions
        void check_assumptions_sanity();
        void unfill_assumptions_set();

        //Needed for tests around renumbering
        void rebuildOrderHeap();
        void clear_order_heap()
        {
            order_heap_rand.clear();
        }


        template<bool update_bogoprops>
        void bump_cl_act(Clause* cl);
        void simple_create_learnt_clause(
            PropBy confl,
            vector<Lit>& out_learnt,
            bool True_confl
        );

    protected:
        void new_var(const bool bva, const uint32_t orig_outer) override;
        void new_vars(const size_t n) override;
        void save_on_var_memory();
        void reset_temp_cl_num();
        void updateVars(
            const vector<uint32_t>& outerToInter
            , const vector<uint32_t>& interToOuter
        );
        void update_var_decay_vsids();
        void add_in_partial_solving_stats();


        struct AssumptionPair {
            AssumptionPair(const Lit _outer, const Lit _outside):
                lit_outer(_outer)
                , lit_orig_outside(_outside)
            {
            }

            Lit lit_outer;
            Lit lit_orig_outside; //not outer, but outside(!)

            bool operator==(const AssumptionPair& other) const {
                return other.lit_outer == lit_outer &&
                other.lit_orig_outside == lit_orig_outside;
            }

            bool operator<(const AssumptionPair& other) const
            {
                //Yes, we need reverse in terms of inverseness
                return ~lit_outer < ~other.lit_outer;
            }
        };
        void fill_assumptions_set();

        //Note that this array can have the same internal variable more than
        //once, in case one has been replaced with the other. So if var 1 =  var 2
        //and var 1 was set to TRUE and var 2 to be FALSE, then we'll have var 1
        //insided this array twice, once it needs to be set to TRUE and once FALSE
        vector<AssumptionPair> assumptions;

        void update_assump_conflict_to_orig_outside(vector<Lit>& out_conflict);


        //For connection with Solver
        void  resetStats();

        SearchHist hist;

        /////////////////
        //Settings
        Solver*   solver;          ///< Thread control class
        double step_size;

        /////////////////
        // Searching
        /// Search for a given number of conflicts.
        lbool search();
        template<bool update_bogoprops>
        bool  handle_conflict(PropBy confl);// Handles the conflict clause
        void  update_history_stats(size_t backtrack_level, uint32_t glue);
        template<bool update_bogoprops>
        void  attach_and_enqueue_learnt_clause(Clause* cl, bool enq = true);
        void  print_learning_debug_info() const;
        void  print_learnt_clause() const;
        template<bool update_bogoprops>
        void  add_otf_subsume_long_clauses();
        template<bool update_bogoprops>
        void  add_otf_subsume_implicit_clause();
        Clause* handle_last_confl_otf_subsumption(
            Clause* cl
            , const uint32_t glue
            , const bool decision_cl
        );
        template<bool update_bogoprops>
        lbool new_decision();  // Handles the case when decision must be made
        void  check_need_restart();     // Helper function to decide if we need to restart during search
        Lit   pickBranchLit();

        ///////////////
        // Conflicting
        struct SearchParams
        {
            SearchParams()
            {
                clear();
            }

            void clear()
            {
                needToStopSearch = false;
                conflictsDoneThisRestart = 0;
            }

            bool needToStopSearch;
            uint64_t conflictsDoneThisRestart;
            uint64_t max_confl_to_do;
            Restart rest_type = Restart::fixed;
        };
        SearchParams params;
        vector<Lit> learnt_clause;
        vector<Lit> decision_clause;
        template<bool update_bogoprops>
        Clause* analyze_conflict(
            PropBy confl //The conflict that we are investigating
            , uint32_t& out_btlevel  //backtrack level
            , uint32_t &glue         //glue of the learnt clause
        );
        void update_clause_glue_from_analysis(Clause* cl);
        template<bool update_bogoprops>
        void minimize_learnt_clause();
        void watch_based_learnt_minim();
        void minimize_using_permdiff();
        void print_fully_minimized_learnt_clause() const;
        size_t find_backtrack_level_of_learnt();
        template<bool update_bogoprops>
        void bump_var_activities_based_on_implied_by_learnts(const uint32_t backtrack_level);
        Clause* otf_subsume_last_resolved_clause(Clause* last_resolved_long_cl);
        void print_debug_resolution_data(const PropBy confl);
        template<bool update_bogoprops>
        Clause* create_learnt_clause(PropBy confl);
        int pathC;

        vector<uint32_t> implied_by_learnts; //for glue-based extra var activity bumping

        /////////////////
        // Variable activity
        double var_inc_vsids;
        void insert_var_order(const uint32_t x);  ///< Insert a variable in current heap
        void insert_var_order_all(const uint32_t x);  ///< Insert a variable in all heaps


        uint64_t more_red_minim_limit_binary_actual;
        uint64_t more_red_minim_limit_cache_actual;
        const SearchStats& get_stats() const;
        size_t mem_used() const;

        int64_t max_confl_phase;
        int64_t max_confl_this_phase;

        uint64_t next_lev1_reduce;
        uint64_t next_lev2_reduce;
        uint64_t next_lev3_reduce;
        double   var_decay_vsids;

    private:
        //////////////
        // Conflict minimisation
        bool litRedundant(Lit p, uint32_t abstract_levels);
        void recursiveConfClauseMin();
        void normalClMinim();
        MyStack<Lit> analyze_stack;
        uint32_t        abstractLevel(const uint32_t x) const;

        //OTF subsumption during learning
        vector<ClOffset> otf_subsuming_long_cls;
        vector<OTFClause> otf_subsuming_short_cls;
        void check_otf_subsume(const ClOffset offset, Clause& cl);
        void create_otf_subsuming_implicit_clause(const Clause& cl);
        void create_otf_subsuming_long_clause(Clause& cl, ClOffset offset);
        template<bool update_bogoprops>
        Clause* add_literals_from_confl_to_learnt(const PropBy confl, const Lit p);
        void debug_print_resolving_clause(const PropBy confl) const;
        template<bool update_bogoprops>
        void add_lit_to_learnt(Lit lit);
        void analyze_final_confl_with_assumptions(const Lit p, vector<Lit>& out_conflict);
        size_t tmp_learnt_clause_size;
        cl_abst_type tmp_learnt_clause_abst;

        //Restarts
        uint64_t max_confl_per_search_solve_call;
        bool blocked_restart = false;
        void check_blocking_restart();
        uint32_t num_search_called = 0;
        uint64_t lastRestartConfl;
        double luby(double y, int x);
        void adjust_phases_restarts();

        void print_solution_varreplace_status() const;

        ////////////
        // Transitive on-the-fly self-subsuming resolution
        void   minimise_redundant_more_more(vector<Lit>& cl);
        void   binary_based_morem_minim(vector<Lit>& cl);
        void   cache_based_morem_minim(vector<Lit>& cl);
        void   stamp_based_morem_minim(vector<Lit>& cl);

        //Variable activities
        struct VarFilter { ///Filter out vars that have been set or is not decision from heap
            const Searcher* cc;
            const Solver* solver;
            VarFilter(const Searcher* _cc, Solver* _solver) :
                cc(_cc)
                ,solver(_solver)
            {}
            bool operator()(uint32_t var) const;
        };
        friend class Gaussian;
        friend class DistillerLong;
        #ifdef CMS_TESTING_ENABLED
        FRIEND_TEST(SearcherTest, pickpolar_rnd);
        FRIEND_TEST(SearcherTest, pickpolar_pos);
        FRIEND_TEST(SearcherTest, pickpolar_neg);
        FRIEND_TEST(SearcherTest, pickpolar_auto);
        FRIEND_TEST(SearcherTest, pickpolar_auto_not_changed_by_simp);
        #endif

        ///Decay all variables with the specified factor. Implemented by increasing the 'bump' value instead.
        void     varDecayActivity ();
        ///Increase a variable with the current 'bump' value.
        template<bool update_bogoprops>
        void     bump_vsids_var_act(uint32_t v, double mult = 1.0);

        //Clause activites
        double cla_inc;

        template<bool update_bogoprops> void decayClauseAct();
        unsigned guess_clause_array(
            const ClauseStats& glue
            , const uint32_t backtrack_lev
        ) const;

        //Other
        void print_solution_type(const lbool status) const;
        uint64_t next_distill = 0;

        //Picking polarity when doing decision
        bool     pick_polarity(const uint32_t var);

        //Last time we clean()-ed the clauses, the number of zero-depth assigns was this many
        size_t   lastCleanZeroDepthAssigns;

        //Used for on-the-fly subsumption. Does A subsume B?
        //Uses 'seen' to do its work
        bool subset(const vector<Lit>& A, const Clause& B);

        double   startTime; ///<When solve() was started
        SearchStats stats;
};

inline uint32_t Searcher::abstractLevel(const uint32_t x) const
{
    return ((uint32_t)1) << (varData[x].level & 31);
}

inline const SearchStats& Searcher::get_stats() const
{
    return stats;
}

inline const SearchHist& Searcher::getHistory() const
{
    return hist;
}

inline void Searcher::add_in_partial_solving_stats()
{
    stats.cpu_time = cpuTime() - startTime;
}

inline void Searcher::insert_var_order(const uint32_t x)
{
    if (!order_heap_rand.inHeap(x)) {
        order_heap_rand.insert(x);
    }
}

inline void Searcher::insert_var_order_all(const uint32_t x)
{
    order_heap_rand.insert(x);
}

template<bool update_bogoprops>
inline void Searcher::bump_cl_act(Clause* cl)
{
    if (update_bogoprops)
        return;

    assert(!cl->getRemoved());

    double new_val = cla_inc + (double)cl->stats.activity;
    cl->stats.activity = (float)new_val;
    if (max_cl_act < new_val) {
        max_cl_act = new_val;
    }


    if (cl->stats.activity > 1e20F ) {
        for(ClOffset offs: longRedCls[2]) {
            cl_alloc.ptr(offs)->stats.activity *= static_cast<float>(1e-20);
        }
        cla_inc *= 1e-20;
        max_cl_act *= 1e-20;
        assert(cla_inc != 0);
    }
}

template<bool update_bogoprops>
inline void Searcher::decayClauseAct()
{
    if (update_bogoprops)
        return;

    cla_inc *= (1 / conf.clause_decay);
}

inline bool Searcher::pick_polarity(const uint32_t var)
{
    switch(conf.polarity_mode) {
        case PolarityMode::polarmode_weighted: {
            std::uniform_real_distribution<double> unif_dbl(0.0, 1.0);
            double rnd = unif_dbl(mtrand);
            return rnd < varData[var].weight;
        }

        default:
            assert(false);
    }

    return true;
}

template<bool update_bogoprops>
void Searcher::bump_var_activities_based_on_implied_by_learnts(uint32_t backtrack_level) {
    assert(!update_bogoprops);

    for (const uint32_t var :implied_by_learnts) {
        if ((int32_t)varData[var].level >= (int32_t)backtrack_level-1L) {
            bump_vsids_var_act<update_bogoprops>(var, 1.0);
        }
    }
}

template<bool update_bogoprops>
inline void Searcher::bump_vsids_var_act(uint32_t var, double mult)
{
    if (update_bogoprops) {
        return;
    }

    var_act_vsids[var] += var_inc_vsids * mult;
    if (max_vsids_act < var_act_vsids[var]) {
        max_vsids_act = var_act_vsids[var];
    }

    #ifdef SLOW_DEBUG
    bool rescaled = false;
    #endif
    if (var_act_vsids[var] > 1e100) {
        // Rescale:

        for (double& act : var_act_vsids) {
            act *= 1e-100;
        }
        max_vsids_act *= 1e-100;

        #ifdef SLOW_DEBUG
        rescaled = true;
        #endif

        //Reset var_inc
        var_inc_vsids *= 1e-100;
    }

    #ifdef SLOW_DEBUG
    if (rescaled) {
        assert(order_heap_vsids.heap_property());
    }
    #endif
}

#ifdef USE_GAUSS
inline uint32_t Searcher::get_sum_gauss_unit_truths() const
{
    return sum_gauss_unit_truths;
}

inline uint32_t Searcher::get_sum_gauss_called() const
{
    return sum_gauss_called;
}

inline uint32_t Searcher::get_sum_gauss_confl() const
{
    return sum_gauss_confl;
}

inline uint32_t Searcher::get_sum_gauss_prop() const
{
    return sum_gauss_prop;
}
#endif



} //end namespace

#endif //__SEARCHER_H__
