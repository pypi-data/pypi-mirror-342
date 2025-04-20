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

#include "solver.h"

#include <fstream>
#include <cmath>
#include <fcntl.h>
#include <functional>
#include <limits>
#include <string>
#include <algorithm>
#include <vector>
#include <complex>
#include <locale>

#include "varreplacer.h"
#include "time_mem.h"
#include "searcher.h"
#include "occsimplifier.h"
#include "prober.h"
#include "distillerlong.h"
#include "clausecleaner.h"
#include "solutionextender.h"
#include "varupdatehelper.h"
#include "completedetachreattacher.h"
#include "subsumestrengthen.h"
#include "watchalgos.h"
#include "clauseallocator.h"
#include "subsumeimplicit.h"
#include "distillerlongwithimpl.h"
#include "str_impl_w_impl_stamp.h"
#include "reducedb.h"
#include "sccfinder.h"
#include "intree.h"
#include "GitSHA1.h"
#include "trim.h"
#include "streambuffer.h"
#include "gaussian.h"
#include "drat.h"
#include "xorfinder.h"

using namespace CMSGen;
using std::cout;
using std::endl;

//#define DRAT_DEBUG

//#define DEBUG_RENUMBER

//#define DEBUG_IMPLICIT_PAIRS_TRIPLETS

Solver::Solver(const SolverConf *_conf, std::atomic<bool>* _must_interrupt_inter) :
    Searcher(_conf, this, _must_interrupt_inter)
{
    if (conf.doProbe) {
        prober = new Prober(this);
    }
    intree = new InTree(this);

    if (conf.perform_occur_based_simp) {
        occsimplifier = new OccSimplifier(this);
    }
    distill_long_cls = new DistillerLong(this);
    dist_long_with_impl = new DistillerLongWithImpl(this);
    dist_impl_with_impl = new StrImplWImplStamp(this);
    clauseCleaner = new ClauseCleaner(this);
    varReplacer = new VarReplacer(this);
    if (conf.doStrSubImplicit) {
        subsumeImplicit = new SubsumeImplicit(this);
    }
    Searcher::solver = this;
    reduceDB = new ReduceDB(this);

    next_lev1_reduce = conf.every_lev1_reduce;
    next_lev2_reduce =  conf.every_lev2_reduce;

    check_xor_cut_config_sanity();
}

Solver::~Solver()
{
    delete prober;
    delete intree;
    delete occsimplifier;
    delete distill_long_cls;
    delete dist_long_with_impl;
    delete dist_impl_with_impl;
    delete clauseCleaner;
    delete varReplacer;
    delete subsumeImplicit;
    delete reduceDB;
}

bool Solver::add_xor_clause_inter(
    const vector<Lit>& lits
    , bool rhs
    , const bool attach
    , bool addDrat
) {
    assert(ok);
    assert(!attach || qhead == trail.size());
    assert(decisionLevel() == 0);

    vector<Lit> ps(lits);
    for(Lit& lit: ps) {
        if (lit.sign()) {
            rhs ^= true;
            lit ^= true;
        }
    }
    clean_xor_no_prop(ps, rhs);

    if (ps.size() >= (0x01UL << 28)) {
        throw CMSGen::TooLongClauseError();
    }
    //cout << "Cleaned ps is: " << ps << endl;

    if (!ps.empty()) {
        if (ps.size() > 2) {
            xor_clauses_updated = true;
            xorclauses.push_back(Xor(ps, rhs));
        }
        ps[0] ^= rhs;
    } else {
        if (rhs) {
            *drat << add
            << fin;
            ok = false;
        }
        return ok;
    }

    //cout << "without rhs is: " << ps << endl;
    add_every_combination_xor(ps, attach, addDrat);

    return ok;
}

void Solver::add_every_combination_xor(
    const vector<Lit>& lits
    , const bool attach
    , const bool addDrat
) {
    //cout << "add_every_combination got: " << lits << endl;

    size_t at = 0;
    vector<Lit> xorlits;
    Lit lastlit_added = lit_Undef;
    while(at != lits.size()) {
        xorlits.clear();
        size_t last_at = at;
        for(; at < last_at+conf.xor_var_per_cut && at < lits.size(); at++) {
            xorlits.push_back(lits[at]);
        }

        //Connect to old cut
        if (lastlit_added != lit_Undef) {
            xorlits.push_back(lastlit_added);
        } else if (at < lits.size()) {
            xorlits.push_back(lits[at]);
            at++;
        }

        if (at + 1 == lits.size()) {
            xorlits.push_back(lits[at]);
            at++;
        }

        //New lit to connect to next cut
        if (at != lits.size()) {
            new_var(true);
            const uint32_t newvar = nVars()-1;
            varData[newvar].added_for_xor = true;
            const Lit toadd = Lit(newvar, false);
            xorlits.push_back(toadd);
            lastlit_added = toadd;
        }

        add_xor_clause_inter_cleaned_cut(xorlits, attach, addDrat);
        if (!ok)
            break;
    }
}

void Solver::add_xor_clause_inter_cleaned_cut(
    const vector<Lit>& lits
    , const bool attach
    , const bool addDrat
) {
    //cout << "xor_inter_cleaned_cut got: " << lits << endl;
    vector<Lit> new_lits;
    for(size_t i = 0; i < (1ULL<<lits.size()); i++) {
        unsigned bits_set = num_bits_set(i, lits.size());
        if (bits_set % 2 == 0) {
            continue;
        }

        new_lits.clear();
        for(size_t at = 0; at < lits.size(); at++) {
            bool xorwith = (i >> at)&1;
            new_lits.push_back(lits[at] ^ xorwith);
        }
        //cout << "Added. " << new_lits << endl;
        Clause* cl = add_clause_int(new_lits, false, ClauseStats(), attach, NULL, addDrat);
        if (cl) {
            cl->set_used_in_xor(true);
            longIrredCls.push_back(cl_alloc.get_offset(cl));
        }

        if (!ok)
            return;
    }
}

unsigned Solver::num_bits_set(const size_t x, const unsigned max_size) const
{
    unsigned bits_set = 0;
    for(size_t i = 0; i < max_size; i++) {
        if ((x>>i)&1) {
            bits_set++;
        }
    }

    return bits_set;
}


bool Solver::sort_and_clean_clause(
    vector<Lit>& ps
    , const vector<Lit>& origCl
    , const bool red
    , const bool sorted
) {
    if (!sorted) {
        std::sort(ps.begin(), ps.end());
    }
    Lit p = lit_Undef;
    uint32_t i, j;
    for (i = j = 0; i != ps.size(); i++) {
        if (value(ps[i]) == l_True) {
            return false;
        } else if (ps[i] == ~p) {
            if (!red) {
                uint32_t var = p.var();
                var = map_inter_to_outer(var);
                if (undef_must_set_vars.size() < var+1) {
                    undef_must_set_vars.resize(var+1, false);
                }
                undef_must_set_vars[var] = true;
            }
            return false;
        } else if (value(ps[i]) != l_False && ps[i] != p) {
            ps[j++] = p = ps[i];

            if (!fresh_solver && varData[p.var()].removed != Removed::none) {
                cout << "ERROR: clause " << origCl << " contains literal "
                << p << " whose variable has been removed (removal type: "
                << removed_type_to_string(varData[p.var()].removed)
                << " var-updated lit: "
                << varReplacer->get_var_replaced_with(p)
                << ")"
                << endl;

                //Variables that have been eliminated cannot be added internally
                //as part of a clause. That's a bug
                assert(varData[p.var()].removed == Removed::none);
            }
        }
    }
    ps.resize(ps.size() - (i - j));
    return true;
}

/**
@brief Adds a clause to the problem. Should ONLY be called internally

This code is very specific in that it must NOT be called with variables in
"ps" that have been replaced, eliminated, etc. Also, it must not be called
when the wer are in an UNSAT (!ok) state, for example. Use it carefully,
and only internally
*/
Clause* Solver::add_clause_int(
    const vector<Lit>& lits
    , const bool red
    , ClauseStats cl_stats
    , const bool attach_long
    , vector<Lit>* finalLits
    , bool addDrat
    , const Lit drat_first
    , const bool sorted
) {
    assert(ok);
    assert(decisionLevel() == 0);
    assert(!attach_long || qhead == trail.size());
    #ifdef VERBOSE_DEBUG
    cout << "add_clause_int clause " << lits << endl;
    #endif //VERBOSE_DEBUG

    //Make cl_stats sane
    add_clause_int_tmp_cl = lits;
    vector<Lit>& ps = add_clause_int_tmp_cl;
    if (!sort_and_clean_clause(ps, lits, red, sorted)) {
        if (finalLits) {
            finalLits->clear();
        }
        return NULL;
    }

    #ifdef VERBOSE_DEBUG
    cout << "add_clause_int final clause " << ps << endl;
    #endif

    //If caller required final set of lits, return it.
    if (finalLits) {
        *finalLits = ps;
    }

    if (addDrat) {
        size_t i = 0;
        if (drat_first != lit_Undef) {
            for(i = 0; i < ps.size(); i++) {
                if (ps[i] == drat_first) {
                    break;
                }
            }
        }
        std::swap(ps[0], ps[i]);
        *drat << add << ps
        << fin;
        std::swap(ps[0], ps[i]);

    }

    //Handle special cases
    switch (ps.size()) {
        case 0:
            ok = false;
            if (conf.verbosity >= 6) {
                cout
                << "c solver received clause through addClause(): "
                << lits
                << " that became an empty clause at toplevel --> UNSAT"
                << endl;
            }
            return NULL;
        case 1:
            enqueue(ps[0]);
            if (attach_long) {
                ok = (propagate<true>().isNULL());
            }

            return NULL;
        case 2:
            attach_bin_clause(ps[0], ps[1], red);
            return NULL;

        default:
            Clause* c = cl_alloc.Clause_new(ps
            , sumConflicts
            );
            if (red) {
                c->makeRed(cl_stats.glue);
            }
            c->stats = cl_stats;

            //In class 'OccSimplifier' we don't need to attach normall
            if (attach_long) {
                attachClause(*c);
            } else {
                if (red) {
                    litStats.redLits += ps.size();
                } else {
                    litStats.irredLits += ps.size();
                }
            }

            return c;
    }
}

void Solver::attachClause(
    const Clause& cl
    , const bool checkAttach
) {
    #if defined(DRAT_DEBUG) && defined(DRAT)
    if (drat) {
        *drat << add << cl << fin;
    }
    #endif

    //Update stats
    if (cl.red()) {
        litStats.redLits += cl.size();
    } else {
        litStats.irredLits += cl.size();
    }

    //Call Solver's function for heavy-lifting
    PropEngine::attachClause(cl, checkAttach);
}

void Solver::attach_bin_clause(
    const Lit lit1
    , const Lit lit2
    , const bool red
    , const bool checkUnassignedFirst
) {
    #if defined(DRAT_DEBUG)
    *drat << add << lit1 << lit2 << fin;
    #endif

    //Update stats
    if (red) {
        binTri.redBins++;
    } else {
        binTri.irredBins++;
    }

    //Call Solver's function for heavy-lifting
    PropEngine::attach_bin_clause(lit1, lit2, red, checkUnassignedFirst);
}

void Solver::detachClause(const Clause& cl, const bool removeDrat)
{
    if (removeDrat) {
        *drat << del << cl << fin;
    }

    assert(cl.size() > 2);
    detach_modified_clause(cl[0], cl[1], cl.size(), &cl);
}

void Solver::detachClause(const ClOffset offset, const bool removeDrat)
{
    Clause* cl = cl_alloc.ptr(offset);
    detachClause(*cl, removeDrat);
}

void Solver::detach_modified_clause(
    const Lit lit1
    , const Lit lit2
    , const uint32_t origSize
    , const Clause* address
) {
    //Update stats
    if (address->red())
        litStats.redLits -= origSize;
    else
        litStats.irredLits -= origSize;

    //Call heavy-lifter
    PropEngine::detach_modified_clause(lit1, lit2, address);
}

bool Solver::addClauseHelper(vector<Lit>& ps)
{
    //If already UNSAT, just return
    if (!ok)
        return false;

    //Sanity checks
    assert(decisionLevel() == 0);
    assert(qhead == trail.size());

    //Check for too long clauses
    if (ps.size() > (0x01UL << 28)) {
        cout << "Too long clause!" << endl;
        throw CMSGen::TooLongClauseError();
    }

    for (Lit& lit: ps) {
        //Check for too large variable number
        if (lit.var() >= nVarsOuter()) {
            std::cerr
            << "ERROR: Variable " << lit.var() + 1
            << " inserted, but max var is "
            << nVarsOuter()
            << endl;
            assert(false);
            std::exit(-1);
        }

        //Undo var replacement
        if (!fresh_solver) {
            const Lit updated_lit = varReplacer->get_lit_replaced_with_outer(lit);
            if (conf.verbosity >= 12
                && lit != updated_lit
            ) {
                cout
                << "EqLit updating outer lit " << lit
                << " to outer lit " << updated_lit
                << endl;
            }
            lit = updated_lit;

            //Map outer to inter, and add re-variable if need be
            if (map_outer_to_inter(lit).var() >= nVars()) {
                new_var(false, lit.var());
            }
        }
    }

    if (!fresh_solver)
        renumber_outer_to_inter_lits(ps);

    #ifdef SLOW_DEBUG
    //Check renumberer
    for (const Lit lit: ps) {
        const Lit updated_lit = varReplacer->get_lit_replaced_with(lit);
        assert(lit == updated_lit);
    }
    #endif

    //Uneliminate vars
    if (!fresh_solver) {
        for (const Lit lit: ps) {
            if (conf.perform_occur_based_simp
                && varData[lit.var()].removed == Removed::elimed
            ) {
                if (!occsimplifier->uneliminate(lit.var()))
                    return false;
            }
        }
    }

    #ifdef SLOW_DEBUG
    //Check
    for (Lit& lit: ps) {
        const Lit updated_lit = varReplacer->get_lit_replaced_with(lit);
        assert(lit == updated_lit);
    }
    #endif

    return true;
}

bool Solver::addClause(const vector<Lit>& lits, bool red)
{
    vector<Lit> ps = lits;
    return Solver::addClauseInt(ps, red);
}

bool Solver::addClauseInt(vector<Lit>& ps, bool red)
{
    if (conf.perform_occur_based_simp && occsimplifier->getAnythingHasBeenBlocked()) {
        std::cerr
        << "ERROR: Cannot add new clauses to the system if blocking was"
        << " enabled. Turn it off from conf.doBlockClauses"
        << endl;
        std::exit(-1);
    }

    #ifdef VERBOSE_DEBUG
    cout << "Adding clause " << ps << endl;
    #endif //VERBOSE_DEBUG
    const size_t origTrailSize = trail.size();

    if (!addClauseHelper(ps)) {
        return false;
    }

    std::sort(ps.begin(), ps.end());

    vector<Lit> *pFinalCl = NULL;
    if (drat->enabled() || conf.simulate_drat) {
        finalCl_tmp.clear();
        pFinalCl = &finalCl_tmp;
    }
    Clause *cl = add_clause_int(
        ps
        , red
        , ClauseStats() //default stats
        , true //yes, attach
        , pFinalCl
        , false //add drat?
        , lit_Undef
        , true
    );

    //Drat -- We manipulated the clause, delete
    if ((drat->enabled() || conf.simulate_drat)
        && ps != finalCl_tmp
    ) {
        //Dump only if non-empty (UNSAT handled later)
        if (!finalCl_tmp.empty()) {
            *drat << add << finalCl_tmp
            << fin;
        }

        //Empty clause, it's UNSAT
        if (!okay()) {
            *drat << add
            << fin;
        }
        *drat << del << ps << fin;
    }

    if (cl != NULL) {
        ClOffset offset = cl_alloc.get_offset(cl);
        if (!red) {
            longIrredCls.push_back(offset);
        } else {
            cl->stats.which_red_array = 2;
            if (cl->stats.glue <= conf.glue_put_lev0_if_below_or_eq) {
                cl->stats.which_red_array = 0;
            } else if (cl->stats.glue <= conf.glue_put_lev1_if_below_or_eq
                && conf.glue_put_lev1_if_below_or_eq != 0
            ) {
                cl->stats.which_red_array = 1;
            }
            longRedCls[cl->stats.which_red_array].push_back(offset);
        }
    }

    zeroLevAssignsByCNF += trail.size() - origTrailSize;

    return ok;
}

void Solver::test_renumbering() const
{
    //Check if we renumbered the variables in the order such as to make
    //the unknown ones first and the known/eliminated ones second
    bool uninteresting = false;
    bool problem = false;
    for(size_t i = 0; i < nVars(); i++) {
        //cout << "val[" << i << "]: " << value(i);

        if (value(i)  != l_Undef)
            uninteresting = true;

        if (varData[i].removed == Removed::elimed
            || varData[i].removed == Removed::replaced
        ) {
            uninteresting = true;
            //cout << " removed" << endl;
        } else {
            //cout << " non-removed" << endl;
        }

        if (value(i) == l_Undef
            && varData[i].removed != Removed::elimed
            && varData[i].removed != Removed::replaced
            && uninteresting
        ) {
            problem = true;
        }
    }
    assert(!problem && "We renumbered the variables in the wrong order!");
}

void Solver::renumber_clauses(const vector<uint32_t>& outerToInter)
{
    //Clauses' abstractions have to be re-calculated
    for(ClOffset offs: longIrredCls) {
        Clause* cl = cl_alloc.ptr(offs);
        updateLitsMap(*cl, outerToInter);
        cl->setStrenghtened();
    }

    for(auto& lredcls: longRedCls) {
        for(ClOffset off: lredcls) {
            Clause* cl = cl_alloc.ptr(off);
            updateLitsMap(*cl, outerToInter);
            cl->setStrenghtened();
        }
    }

    //Clauses' abstractions have to be re-calculated
    xor_clauses_updated = true;
    for(Xor& x: xorclauses) {
        updateVarsMap(x, outerToInter);
    }
}

size_t Solver::calculate_interToOuter_and_outerToInter(
    vector<uint32_t>& outerToInter
    , vector<uint32_t>& interToOuter
) {
    size_t at = 0;
    vector<uint32_t> useless;
    size_t numEffectiveVars = 0;
    for(size_t i = 0; i < nVars(); i++) {
        if (value(i) != l_Undef
            || varData[i].removed == Removed::elimed
            || varData[i].removed == Removed::replaced
        ) {
            useless.push_back(i);
            continue;
        }

        outerToInter[i] = at;
        interToOuter[at] = i;
        at++;
        numEffectiveVars++;
    }

    //Fill the rest with variables that have been removed/eliminated/set
    for(vector<uint32_t>::const_iterator
        it = useless.begin(), end = useless.end()
        ; it != end
        ; ++it
    ) {
        outerToInter[*it] = at;
        interToOuter[at] = *it;
        at++;
    }
    assert(at == nVars());

    //Extend to nVarsOuter() --> these are just the identity transformation
    for(size_t i = nVars(); i < nVarsOuter(); i++) {
        outerToInter[i] = i;
        interToOuter[i] = i;
    }

    return numEffectiveVars;
}

double Solver::calc_renumber_saving()
{
    uint32_t num_used = 0;
    for(size_t i = 0; i < nVars(); i++) {
        if (value(i) != l_Undef
            || varData[i].removed == Removed::elimed
            || varData[i].removed == Removed::replaced
        ) {
            continue;
        }
        num_used++;
    }
    double saving = 1.0-(double)num_used/(double)nVars();
    return saving;
}

bool Solver::clean_xor_clauses_from_duplicate_and_set_vars()
{
    assert(decisionLevel() == 0);
    double myTime = cpuTime();
    XorFinder f(NULL, this);
    for(Xor& x: xorclauses) {
        solver->clean_xor_vars_no_prop(x.get_vars(), x.rhs);
        if (x.size() == 0 && x.rhs == true) {
            ok = false;
            break;
        }
    }

    const double time_used = cpuTime() - myTime;
    if (conf.verbosity) {
        cout
        << "c [xor-clean]"
        << conf.print_times(time_used)
        << endl;
    }

    return okay();
}

//Beware. Cannot be called while Searcher is running.
bool Solver::renumber_variables(bool must_renumber)
{
    assert(okay());
    assert(decisionLevel() == 0);
    if (nVars() == 0) {
        return okay();
    }

    if (!must_renumber
        && calc_renumber_saving() < 0.2
    ) {
        return okay();
    }

    #ifdef USE_GAUSS
    solver->clear_gauss_matrices();
    #endif

    double myTime = cpuTime();
    clauseCleaner->remove_and_clean_all();
    if (!xorclauses.empty()) {
        if (!clean_xor_clauses_from_duplicate_and_set_vars())
            return false;
    }

    //outerToInter[10] = 0 ---> what was 10 is now 0.
    vector<uint32_t> outerToInter(nVarsOuter());
    vector<uint32_t> interToOuter(nVarsOuter());

    size_t numEffectiveVars =
        calculate_interToOuter_and_outerToInter(outerToInter, interToOuter);

    //Create temporary outerToInter2
    vector<uint32_t> interToOuter2(nVarsOuter()*2);
    for(size_t i = 0; i < nVarsOuter(); i++) {
        interToOuter2[i*2] = interToOuter[i]*2;
        interToOuter2[i*2+1] = interToOuter[i]*2+1;
    }

    renumber_clauses(outerToInter);
    CNF::updateVars(outerToInter, interToOuter);
    PropEngine::updateVars(outerToInter, interToOuter, interToOuter2);
    Searcher::updateVars(outerToInter, interToOuter);

    if (conf.doStamp) {
        stamp.updateVars(outerToInter, interToOuter2, seen);
    }

    //Update sub-elements' vars
    varReplacer->updateVars(outerToInter, interToOuter);
    if (conf.doCache) {
        implCache.updateVars(seen, outerToInter, interToOuter2, numEffectiveVars);
    }

    //Tests
    test_renumbering();
    test_reflectivity_of_renumbering();

    //Print results
    const double time_used = cpuTime() - myTime;
    if (conf.verbosity) {
        cout
        << "c [renumber]"
        << conf.print_times(time_used)
        << endl;
    }

    if (conf.doSaveMem) {
        save_on_var_memory(numEffectiveVars);
    }

    //NOTE order heap is now wrong, but that's OK, it will be restored from
    //backed up activities and then rebuilt at the start of Searcher

    return okay();
}

void Solver::check_switchoff_limits_newvar(size_t n)
{
    if (conf.doStamp
        && nVars() + n > 15ULL*1000ULL*1000ULL*conf.var_and_mem_out_mult //~1 GB of RAM
    ) {
        conf.doStamp = false;
        stamp.freeMem();
        if (conf.verbosity) {
            cout
            << "c Switching off stamping due to excessive number of variables"
            << " (it would take too much memory)"
            << endl;
        }
    }

    if (conf.doCache
        && nVars() + n > 5ULL*1000ULL*1000ULL*conf.var_and_mem_out_mult
    ) {
        conf.doCache = false;
        implCache.free();

        if (conf.verbosity) {
            cout
            << "c Switching off caching due to excessive number of variables"
            << " (it would take too much memory)"
            << endl;
        }
    }
}

void Solver::new_vars(size_t n)
{
    if (n == 0) {
        return;
    }

    check_switchoff_limits_newvar(n);
    Searcher::new_vars(n);
    varReplacer->new_vars(n);

    if (conf.perform_occur_based_simp) {
        occsimplifier->new_vars(n);
    }
}

void Solver::new_var(const bool bva, const uint32_t orig_outer)
{
    check_switchoff_limits_newvar();
    Searcher::new_var(bva, orig_outer);

    varReplacer->new_var(orig_outer);

    if (conf.perform_occur_based_simp) {
        occsimplifier->new_var(orig_outer);
    }

    //Too expensive
    //test_reflectivity_of_renumbering();
}

void Solver::save_on_var_memory(const uint32_t newNumVars)
{
    //print_mem_stats();
    minNumVars = newNumVars;
    Searcher::save_on_var_memory();

    varReplacer->save_on_var_memory();
    if (occsimplifier) {
        occsimplifier->save_on_var_memory();
    }
    //print_mem_stats();
}

void Solver::set_assumptions()
{
    assert(assumptions.empty());
    #ifdef SLOW_DEBUG
    for(auto x: varData) {
        assert(x.assumption == l_Undef);
    }
    #endif

    conflict.clear();
    back_number_from_outside_to_outer(outside_assumptions);
    vector<Lit> inter_assumptions = back_number_from_outside_to_outer_tmp;
    addClauseHelper(inter_assumptions);
    assert(inter_assumptions.size() == outside_assumptions.size());

    for(size_t i = 0; i < inter_assumptions.size(); i++) {
        Lit outside_lit = lit_Undef;
        const Lit inter_lit = inter_assumptions[i];
        if (i < outside_assumptions.size()) {
            outside_lit = outside_assumptions[i];
        }

        const Lit outer_lit = map_inter_to_outer(inter_lit);
        assumptions.push_back(AssumptionPair(outer_lit, outside_lit));
    }

    fill_assumptions_set();
}

void Solver::add_assumption(const Lit assump)
{
    assert(varData[assump.var()].assumption == l_Undef);
    assert(varData[assump.var()].removed == Removed::none);
    assert(value(assump) == l_Undef);

    Lit outer_lit = map_inter_to_outer(assump);
    assumptions.push_back(AssumptionPair(outer_lit, lit_Undef));
    varData[assump.var()].assumption = assump.sign() ? l_False : l_True;
}

void Solver::check_model_for_assumptions() const
{
    for(const AssumptionPair& lit_pair: assumptions) {
        const Lit outside_lit = lit_pair.lit_orig_outside;
        if (outside_lit.var() == var_Undef) {
            //This is an assumption that is a BVA variable
            //Currently, this can only be BreakID
            continue;
        }
        assert(outside_lit.var() < model.size());

        if (model_value(outside_lit) == l_Undef) {
            std::cerr
            << "ERROR, lit " << outside_lit
            << " was in the assumptions, but it wasn't set at all!"
            << endl;
        }
        assert(model_value(outside_lit) != l_Undef);

        if (model_value(outside_lit) != l_True) {
            std::cerr
            << "ERROR, lit " << outside_lit
            << " was in the assumptions, but it was set to: "
            << model_value(outside_lit)
            << endl;
        }
        assert(model_value(outside_lit) == l_True);
    }
}

void Solver::check_recursive_minimization_effectiveness(const lbool status)
{
    const SearchStats& srch_stats = Searcher::get_stats();
    if (status == l_Undef
        && conf.doRecursiveMinim
        && srch_stats.recMinLitRem + srch_stats.litsRedNonMin > 100000
    ) {
        double remPercent =
            float_div(srch_stats.recMinLitRem, srch_stats.litsRedNonMin)*100.0;

        double costPerGained = float_div(srch_stats.recMinimCost, remPercent);
        if (costPerGained > 200ULL*1000ULL*1000ULL) {
            conf.doRecursiveMinim = false;
            if (conf.verbosity) {
                cout
                << "c recursive minimization too costly: "
                << std::fixed << std::setprecision(0) << (costPerGained/1000.0)
                << "Kcost/(% lits removed) --> disabling"
                << std::setprecision(2)
                << endl;
            }
        } else {
            if (conf.verbosity) {
                cout
                << "c recursive minimization cost OK: "
                << std::fixed << std::setprecision(0) << (costPerGained/1000.0)
                << "Kcost/(% lits removed)"
                << std::setprecision(2)
                << endl;
            }
        }
    }
}

void Solver::check_minimization_effectiveness(const lbool status)
{
    const SearchStats& search_stats = Searcher::get_stats();
    if (status == l_Undef
        && conf.doMinimRedMore
        && search_stats.moreMinimLitsStart > 100000
    ) {
        double remPercent = float_div(
            search_stats.moreMinimLitsStart-search_stats.moreMinimLitsEnd,
            search_stats.moreMinimLitsStart)*100.0;

        //TODO take into account the limit on the number of first literals, too
        if (remPercent < 1.0) {
            conf.doMinimRedMore = false;
            if (conf.verbosity) {
                cout
                << "c more minimization effectiveness low: "
                << std::fixed << std::setprecision(2) << remPercent
                << " % lits removed --> disabling"
                << endl;
            }
        } else if (remPercent > 7.0) {
            more_red_minim_limit_binary_actual = 3*conf.more_red_minim_limit_binary;
            more_red_minim_limit_cache_actual  = 3*conf.more_red_minim_limit_cache;
            if (conf.verbosity) {
                cout
                << "c more minimization effectiveness good: "
                << std::fixed << std::setprecision(2) << remPercent
                << " % --> increasing limit to 3x"
                << endl;
            }
        } else {
            more_red_minim_limit_binary_actual = conf.more_red_minim_limit_binary;
            more_red_minim_limit_cache_actual  = conf.more_red_minim_limit_cache;
            if (conf.verbosity) {
                cout
                << "c more minimization effectiveness OK: "
                << std::fixed << std::setprecision(2) << remPercent
                << " % --> setting limit to norm"
                << endl;
            }
        }
    }
}

void Solver::extend_solution(const bool only_sampling_solution)
{
    #ifdef DEBUG_IMPLICIT_STATS
    check_stats();
    #endif

    #ifdef SLOW_DEBUG
    //Check that sampling vars are all assigned
    if (conf.sampling_vars) {
        for(uint32_t outside_var: *conf.sampling_vars) {
            uint32_t outer_var = map_to_with_bva(outside_var);
            outer_var = varReplacer->get_var_replaced_with_outer(outer_var);
            uint32_t int_var = map_outer_to_inter(outer_var);

            assert(varData[int_var].removed == Removed::none ||
                varData[int_var].removed == Removed::decomposed);

            if (int_var < nVars() && varData[int_var].removed == Removed::none) {
                assert(model[int_var] != l_Undef);
            }
        }
    }
    #endif

    model = back_number_solution_from_inter_to_outer(model);
    if (conf.need_decisions_reaching) {
        map_inter_to_outer(decisions_reaching_model);
    }

    if (!only_sampling_solution) {
        SolutionExtender extender(this, occsimplifier);
        extender.extend();
    } else {
        solver->varReplacer->extend_model_already_set();
    }

    //map back without BVA
    model = map_back_to_without_bva(model);
    if (conf.need_decisions_reaching) {
        decisions_reaching_model_valid = true;
        const vector<uint32_t> my_map = build_outer_to_without_bva_map();
        updateLitsMap(decisions_reaching_model, my_map);
        for(const Lit lit: decisions_reaching_model) {
            if (lit.var() >= nVarsOutside()) {
                decisions_reaching_model_valid = false;
            }
        }
    }

    if (only_sampling_solution) {
        assert(conf.sampling_vars);
        for(uint32_t var: *conf.sampling_vars) {
            if (model[var] == l_Undef) {
                cout << "ERROR: variable " << var+1 << " is set as sampling but is unset!" << endl;
                cout << "NOTE: var " << var + 1 << " has removed value: "
                << removed_type_to_string(varData[var].removed)
                << " and is set to " << value(var) << endl;
            }
            assert(model[var] != l_Undef);
        }
    }

    check_model_for_assumptions();
}

void Solver::check_xor_cut_config_sanity() const
{
    if (conf.xor_var_per_cut < 1) {
        std::cerr << "ERROR: Too low cutting number: " << conf.xor_var_per_cut << ". Needs to be at least 1." << endl;
        exit(-1);
    }

    if (MAX_XOR_RECOVER_SIZE < 4) {
        std::cerr << "ERROR: MAX_XOR_RECOVER_SIZE  must be at least 4. It's currently: " << MAX_XOR_RECOVER_SIZE << endl;
        exit(-1);
    }

    if (conf.xor_var_per_cut+2 > MAX_XOR_RECOVER_SIZE) {
        std::cerr << "ERROR: Too high cutting number, we will not be able to recover cut XORs due to MAX_XOR_RECOVER_SIZE only being " << MAX_XOR_RECOVER_SIZE << endl;
        exit(-1);
    }
}

void Solver::check_config_parameters() const
{
    if (conf.max_confl < 0) {
        std::cerr << "ERROR: Maximum number conflicts set must be greater or equal to 0" << endl;
        exit(-1);
    }

    if (conf.shortTermHistorySize <= 0) {
        std::cerr << "ERROR: You MUST give a short term history size (\"--gluehist\")  greater than 0!" << endl;
        exit(-1);
    }

    #ifdef USE_GAUSS
    if ((drat->enabled() || solver->conf.simulate_drat) &&
        conf.gaussconf.enabled
    )  {
        std::cerr << "ERROR: Cannot have both DRAT and GAUSS on at the same time!" << endl;
        exit(-1);
    }
    #endif

    #ifdef SLOW_DEBUG
    if (solver->conf.sampling_vars)
    {
        for(uint32_t v: *solver->conf.sampling_vars) {
            assert(v < nVarsOutside());
        }
    }
    #endif

    if (conf.blocking_restart_trail_hist_length == 0) {
        std::cerr << "ERROR: Blocking restart length must be at least 0" << endl;
        exit(-1);
    }
    check_xor_cut_config_sanity();
}

lbool Solver::simplify_problem_outside()
{
    #ifdef SLOW_DEBUG
    if (ok) {
        assert(check_order_heap_sanity());
        check_implicit_stats();
        check_wrong_attach();
        find_all_attach();
        test_all_clause_attached();
    }
    #endif
    decisions_reaching_model.clear();
    decisions_reaching_model_valid = false;

    conf.global_timeout_multiplier = conf.orig_global_timeout_multiplier;
    solveStats.num_simplify_this_solve_call = 0;
    set_assumptions();

    lbool status = l_Undef;
    if (!ok) {
        status = l_False;
        goto end;
    }
    check_config_parameters();

    if (nVars() > 0 && conf.do_simplify_problem) {
        status = simplify_problem(false);
    }

    end:
    unfill_assumptions_set();
    assumptions.clear();
    return status;
}

lbool Solver::solve_with_assumptions(
    const vector<Lit>* _assumptions,
    const bool only_sampling_solution
) {
    fresh_solver = false;
    decisions_reaching_model.clear();
    decisions_reaching_model_valid = false;
    move_to_outside_assumps(_assumptions);
    set_assumptions();
    #ifdef SLOW_DEBUG
    if (ok) {
        assert(check_order_heap_sanity());
        check_implicit_stats();
        find_all_attach();
        check_no_duplicate_lits_anywhere();
    }
    #endif

    solveStats.num_solve_calls++;
    check_config_parameters();
    luby_loop_num = 0;

    //Reset parameters
    max_confl_phase = conf.restart_first;
    max_confl_this_phase = max_confl_phase;
    var_decay_vsids = conf.var_decay_vsids_start;
    step_size = conf.orig_step_size;
    conf.global_timeout_multiplier = conf.orig_global_timeout_multiplier;
    solveStats.num_simplify_this_solve_call = 0;
    params.rest_type = conf.restartType;
    if (conf.verbosity >= 6) {
        cout << "c " << __func__ << " called" << endl;
    }

    //Check if adding the clauses caused UNSAT
    lbool status = l_Undef;
    if (!ok) {
        assert(conflict.empty());
        status = l_False;
        if (conf.verbosity >= 6) {
            cout << "c Solver status " << status << " on startup of solve()" << endl;
        }
        goto end;
    }
    assert(prop_at_head());
    assert(okay());

    //If still unknown, simplify
    if (status == l_Undef
        && nVars() > 0
        && conf.do_simplify_problem
        && conf.simplify_at_startup
        && (solveStats.num_simplify == 0 || conf.simplify_at_every_startup)
    ) {
        status = simplify_problem(!conf.full_simplify_at_startup);
    }

    if (status == l_Undef) {
        status = iterate_until_solved();
    }

    end:

    handle_found_solution(status, only_sampling_solution);
    unfill_assumptions_set();
    assumptions.clear();
    conf.max_confl = std::numeric_limits<long>::max();
    conf.maxTime = std::numeric_limits<double>::max();
    drat->flush();
    return status;
}

long Solver::calc_num_confl_to_do_this_iter(const size_t iteration_num) const
{
    double iter_num = std::min<size_t>(iteration_num, 100ULL);
    double mult = std::pow(conf.num_conflicts_of_search_inc, iter_num);
    mult = std::min(mult, conf.num_conflicts_of_search_inc_max);
    long num_conflicts_of_search = (double)conf.num_conflicts_of_search*mult;
    if (conf.never_stop_search) {
        num_conflicts_of_search = 500ULL*1000ULL*1000ULL;
    }
    num_conflicts_of_search = std::min<long>(
        num_conflicts_of_search
        , (long)conf.max_confl - (long)sumConflicts
    );

    return num_conflicts_of_search;
}

lbool Solver::iterate_until_solved()
{
    size_t iteration_num = 0;
    lbool status = l_Undef;
    while (status == l_Undef
        && !must_interrupt_asap()
        && cpuTime() < conf.maxTime
        && sumConflicts < (uint64_t)conf.max_confl
    ) {
        iteration_num++;
        if (conf.verbosity && iteration_num >= 2) {
            print_clause_size_distrib();
        }

        const long num_confl = calc_num_confl_to_do_this_iter(iteration_num);
        if (num_confl <= 0) {
            break;
        }
        status = Searcher::solve(num_confl);

        //Check for effectiveness
        check_recursive_minimization_effectiveness(status);
        check_minimization_effectiveness(status);

        //Update stats
        sumSearchStats += Searcher::get_stats();
        sumPropStats += propStats;
        propStats.clear();
        Searcher::resetStats();
        check_too_many_low_glues();

        //Solution has been found
        if (status != l_Undef) {
            break;
        }

        //If we are over the limit, exit
        if (sumConflicts >= (uint64_t)conf.max_confl
            || cpuTime() > conf.maxTime
            || must_interrupt_asap()
        ) {
            break;
        }

        if (conf.do_simplify_problem) {
            status = simplify_problem(false);
        }
    }
    return status;
}

void Solver::check_too_many_low_glues()
{
    if (conf.glue_put_lev0_if_below_or_eq == 2
        || sumConflicts < conf.min_num_confl_adjust_glue_cutoff
        || adjusted_glue_cutoff_if_too_many
        || conf.adjust_glue_if_too_many_low >= 1.0
    ) {
        return;
    }

    double perc = float_div(sumSearchStats.red_cl_in_which0, sumConflicts);
    if (perc > conf.adjust_glue_if_too_many_low) {
        conf.glue_put_lev0_if_below_or_eq--;
        adjusted_glue_cutoff_if_too_many = true;
        if (conf.verbosity) {
            cout << "c Adjusted glue cutoff to " << conf.glue_put_lev0_if_below_or_eq
            << " due to too many low glues: " << perc*100.0 << " %" << endl;
        }
    }
}

void Solver::handle_found_solution(const lbool status, const bool only_sampling_solution)
{
    if (status == l_True) {
        extend_solution(only_sampling_solution);
        cancelUntil(0);

        #ifdef DEBUG_ATTACH_MORE
        find_all_attach();
        test_all_clause_attached();
        #endif
    } else if (status == l_False) {
        cancelUntil(0);

        for(const Lit lit: conflict) {
            if (value(lit) == l_Undef) {
                assert(var_inside_assumptions(lit.var()) != l_Undef);
            }
        }
        update_assump_conflict_to_orig_outside(conflict);
    }

    //Too slow when running lots of small queries
    #ifdef DEBUG_IMPLICIT_STATS
    check_implicit_stats();
    #endif
}

lbool Solver::execute_inprocess_strategy(
    const bool startup
    , const string& strategy
) {
    //std::string input = "abc,def,ghi";
    std::istringstream ss(strategy + ", ");
    std::string token;
    std::string occ_strategy_tokens;

    while(std::getline(ss, token, ',')) {
        if (sumConflicts >= (uint64_t)conf.max_confl
            || cpuTime() > conf.maxTime
            || must_interrupt_asap()
            || nVars() == 0
            || !okay()
        ) {
            break;
        }

        assert(watches.get_smudged_list().empty());
        assert(prop_at_head());
        assert(okay());
        check_wrong_attach();
        #ifdef SLOW_DEBUG
        check_stats();
        check_no_duplicate_lits_anywhere();
        check_assumptions_sanity();
        #endif

        token = trim(token);
        std::transform(token.begin(), token.end(), token.begin(), ::tolower);
        if (!occ_strategy_tokens.empty() && token.substr(0,3) != "occ") {
            if (conf.perform_occur_based_simp
                && occsimplifier
            ) {
                occ_strategy_tokens = trim(occ_strategy_tokens);
                if (conf.verbosity) {
                    cout << "c --> Executing OCC strategy token(s): '"
                    << occ_strategy_tokens << "'\n";
                }
                occsimplifier->simplify(startup, occ_strategy_tokens);
            }
            occ_strategy_tokens.clear();
            if (sumConflicts >= (uint64_t)conf.max_confl
                || cpuTime() > conf.maxTime
                || must_interrupt_asap()
                || nVars() == 0
                || !ok
            ) {
                break;
            }
            #ifdef SLOW_DEBUG
            solver->check_stats();
            check_assumptions_sanity();
            #endif
        }

        if (conf.verbosity && token.substr(0,3) != "occ" && token != "") {
            cout << "c --> Executing strategy token: " << token << '\n';
        }

        if (token == "scc-vrepl") {
            if (conf.doFindAndReplaceEqLits) {
                varReplacer->replace_if_enough_is_found(
                    std::floor((double)get_num_free_vars()*0.001));
            }
        } else if (token == "cache-clean") {
            if (conf.doCache) {
                implCache.clean(this);
            }
        } else if (token == "cache-tryboth") {
            if (conf.doCache) {
                implCache.tryBoth(this);
            }
        } else if (token == "sub-impl") {
            //subsume BIN with BIN
            if (conf.doStrSubImplicit) {
                subsumeImplicit->subsume_implicit();
            }
        } else if (token == "intree-probe") {
            if (conf.doIntreeProbe) {
                intree->intree_probe();
            }
        } else if (token == "probe") {
            if (conf.doProbe)
                prober->probe();
        } else if (token == "sub-str-cls-with-bin") {
            //Subsumes and strengthens long clauses with binary clauses
            if (conf.do_distill_clauses) {
                dist_long_with_impl->distill_long_with_implicit(true);
            }
        } else if (token == "sub-cls-with-bin") {
            //Subsumes and strengthens long clauses with binary clauses
            if (conf.do_distill_clauses) {
                dist_long_with_impl->distill_long_with_implicit(false);
            }
        } else if (token == "distill-cls") {
            //Enqueues literals in long + tri clauses two-by-two and propagates
            if (conf.do_distill_clauses) {
                distill_long_cls->distill(false);
            }
        } else if (token == "str-impl") {
            //Strengthens BIN&TRI with BIN&TRI
            if (conf.doStrSubImplicit) {
                dist_impl_with_impl->str_impl_w_impl_stamp();
            }
        } else if (token == "check-cache-size") {
            //Delete and disable cache if too large
            if (conf.doCache) {
                const size_t memUsedMB = implCache.mem_used()/(1024UL*1024UL);
                if (memUsedMB > conf.maxCacheSizeMB) {
                    if (conf.verbosity) {
                        cout
                        << "c Turning off cache, memory used, "
                        << memUsedMB << " MB"
                        << " is over limit of " << conf.maxCacheSizeMB  << " MB"
                        << endl;
                    }
                    implCache.free();
                    conf.doCache = false;
                }
            }
        } else if (token == "cl-consolidate") {
            cl_alloc.consolidate(this, false, true);
        } else if (token == "renumber" || token == "must-renumber") {
            if (conf.doRenumberVars) {
                //Clean cache before renumber -- very important, otherwise
                //we will be left with lits inside the cache that are out-of-bounds
                if (conf.doCache) {
                    bool setSomething = true;
                    while(setSomething) {
                        if (!implCache.clean(this, &setSomething))
                            return l_False;
                    }
                }

                if (!renumber_variables(token == "must-renumber" || conf.must_renumber)) {
                    return l_False;
                }
            }
        } else if (token == "") {
            //Nothing, just an empty comma, ignore
        } else if (token.substr(0,3) == "occ") {
            occ_strategy_tokens += token + ", ";
            //cout << "occ_strategy_tokens now: " << occ_strategy_tokens  << endl;
        } else {
            cout << "ERROR: strategy '" << token << "' not recognised!" << endl;
            exit(-1);
        }

        #ifdef SLOW_DEBUG
        check_stats();
        #endif

        if (!ok) {
            return l_False;
        }
        check_wrong_attach();
    }

    return ok ? l_Undef : l_False;
}

/**
@brief The function that brings together almost all CNF-simplifications
*/
lbool Solver::simplify_problem(const bool startup)
{
    assert(ok);
    #ifdef DEBUG_IMPLICIT_STATS
    check_stats();
    #endif
    #ifdef DEBUG_ATTACH_MORE
    test_all_clause_attached();
    find_all_attach();
    assert(check_order_heap_sanity());
    #endif
    #ifdef DEBUG_MARKED_CLAUSE
    assert(solver->no_marked_clauses());
    #endif

    if (solveStats.num_simplify_this_solve_call >= conf.max_num_simplify_per_solve_call) {
        return l_Undef;
    }

    clear_order_heap();
    #ifdef USE_GAUSS
    clear_gauss_matrices();
    #endif

    if (conf.verbosity >= 6) {
        cout
        << "c " <<  __func__ << " called"
        << endl;
    }

    lbool ret;
    if (startup) {
        ret = execute_inprocess_strategy(startup, conf.simplify_schedule_startup);
    } else {
        ret = execute_inprocess_strategy(startup, conf.simplify_schedule_nonstartup);
    }

    //Free unused watch memory
    free_unused_watches();

    if (conf.verbosity >= 6) {
        cout << "c " << __func__ << " finished" << endl;
    }
    conf.global_timeout_multiplier *= conf.global_timeout_multiplier_multiplier;
    conf.global_timeout_multiplier =
        std::min<double>(
            conf.global_timeout_multiplier,
            conf.orig_global_timeout_multiplier*conf.global_multiplier_multiplier_max
        );
    if (conf.verbosity)
        cout << "c global_timeout_multiplier: " << conf. global_timeout_multiplier << endl;

    solveStats.num_simplify++;
    solveStats.num_simplify_this_solve_call++;

    assert(!(ok == false && ret != l_False));
    if (!ok || ret == l_False) {
        return l_False;
    } else if (ret == l_Undef) {
        check_stats();
        check_implicit_propagated();
        rebuildOrderHeap();
        #ifdef DEBUG_ATTACH_MORE
        find_all_attach();
        test_all_clause_attached();
        #endif
        check_wrong_attach();

        return ret;
    } else {
        assert(ret == l_True);
        rebuildOrderHeap();
        finish_up_solve(ret);
        return ret;
    }
}

void Solver::print_prop_confl_stats(
    std::string name
    , const vector<ClauseUsageStats>& cl_usage_stats
) const {
    for(size_t i = 0; i < cl_usage_stats.size(); i++) {
        //Nothing to do here, no stats really
        if (cl_usage_stats[i].num == 0)
            continue;

        cout
        << name << " : " << std::setw(4) << i
        << " Avg. props: " << std::setw(6) << std::fixed << std::setprecision(2)
        << float_div(cl_usage_stats[i].sumProp, cl_usage_stats[i].num);

        cout
        << name << " : " << std::setw(4) << i
        << " Avg. confls: " << std::setw(6) << std::fixed << std::setprecision(2)
        << float_div(cl_usage_stats[i].sumConfl, cl_usage_stats[i].num);

        if (cl_usage_stats[i].sumLookedAt > 0) {
            cout
            << " Props&confls/looked at: " << std::setw(6) << std::fixed << std::setprecision(2)
            << float_div(cl_usage_stats[i].sumPropAndConfl(), cl_usage_stats[i].sumLookedAt);
        }

        cout << endl;
    }
}

void CMSGen::Solver::print_stats(const double cpu_time, const double cpu_time_total) const
{
    if (conf.verbStats >= 1) {
        cout << "c ------- FINAL TOTAL SEARCH STATS ---------" << endl;
    }

    if (conf.do_print_times) {
        print_stats_line("c UIP search time"
            , sumSearchStats.cpu_time
            , stats_line_percent(sumSearchStats.cpu_time, cpu_time)
            , "% time"
        );
    }

    if (conf.verbStats >= 3) {
        print_full_restart_stat(cpu_time, cpu_time_total);
    } else if (conf.verbStats == 2) {
        print_norm_stats(cpu_time, cpu_time_total);
    } else if (conf.verbStats == 1) {
        print_min_stats(cpu_time, cpu_time_total);
    }
}

void Solver::print_min_stats(const double cpu_time, const double cpu_time_total) const
{
    sumSearchStats.print_short(sumPropStats.propagations, conf.do_print_times);
    print_stats_line("c props/decision"
        , float_div(propStats.propagations, sumSearchStats.decisions)
    );
    print_stats_line("c props/conflict"
        , float_div(propStats.propagations, sumConflicts)
    );

    print_stats_line("c 0-depth assigns", trail.size()
        , stats_line_percent(trail.size(), nVars())
        , "% vars"
    );

    //Failed lit stats
    if (conf.doProbe) {
        if (conf.do_print_times)
        print_stats_line("c probing time"
            , prober->get_stats().cpu_time
            , stats_line_percent(prober->get_stats().cpu_time, cpu_time)
            , "% time"
        );
    }
    //OccSimplifier stats
    if (conf.perform_occur_based_simp) {
        if (conf.do_print_times)
            print_stats_line("c OccSimplifier time"
            , occsimplifier->get_stats().total_time(occsimplifier)
            , stats_line_percent(occsimplifier->get_stats().total_time(occsimplifier) ,cpu_time)
            , "% time"
        );
        occsimplifier->get_sub_str()->get_stats().print_short(this);
    }
    if (conf.do_print_times)
        print_stats_line("c SCC time"
        , varReplacer->get_scc_finder()->get_stats().cpu_time
        , stats_line_percent(varReplacer->get_scc_finder()->get_stats().cpu_time, cpu_time)
        , "% time"
    );
    varReplacer->get_scc_finder()->get_stats().print_short(NULL);

    //varReplacer->get_stats().print_short(nVars());
    if (conf.do_print_times)
        print_stats_line("c distill time"
                    , distill_long_cls->get_stats().time_used
                    , stats_line_percent(distill_long_cls->get_stats().time_used, cpu_time)
                    , "% time"
    );
    if (conf.do_print_times)
        print_stats_line("c strength cache-irred time"
                    , dist_long_with_impl->get_stats().irredCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().irredCacheBased.cpu_time, cpu_time)
                    , "% time"
    );
    if (conf.do_print_times)
        print_stats_line("c strength cache-red time"
                    , dist_long_with_impl->get_stats().redCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().redCacheBased.cpu_time, cpu_time)
                    , "% time"
    );

    if (conf.do_print_times) {
        print_stats_line("c Conflicts in UIP"
            , sumConflicts
            , float_div(sumConflicts, cpu_time)
            , "confl/time_this_thread"
        );
    } else {
        print_stats_line("c Conflicts in UIP", sumConflicts);
    }
    print_stats_time(cpu_time, cpu_time_total);
    double vm_usage;
    print_stats_line("c Mem used"
        , (double)memUsedTotal(vm_usage)/(1024UL*1024UL)
        , "MB"
    );
}

void Solver::print_stats_time(const double cpu_time, const double cpu_time_total) const
{
    if (conf.do_print_times) {
        print_stats_line("c Total time (this thread)", cpu_time);
        if (cpu_time != cpu_time_total)
            print_stats_line("c Total time (all threads)", cpu_time_total);
    }
}

void Solver::print_norm_stats(const double cpu_time, const double cpu_time_total) const
{
    sumSearchStats.print_short(sumPropStats.propagations, conf.do_print_times);
    print_stats_line("c props/decision"
        , float_div(propStats.propagations, sumSearchStats.decisions)
    );
    print_stats_line("c props/conflict"
        , float_div(propStats.propagations, sumConflicts)
    );

    print_stats_line("c 0-depth assigns", trail.size()
        , stats_line_percent(trail.size(), nVars())
        , "% vars"
    );
    print_stats_line("c 0-depth assigns by CNF"
        , zeroLevAssignsByCNF
        , stats_line_percent(zeroLevAssignsByCNF, nVars())
        , "% vars"
    );

    print_stats_line("c reduceDB time"
        , reduceDB->get_total_time()
        , stats_line_percent(reduceDB->get_total_time(), cpu_time)
        , "% time"
    );

    //Failed lit stats
    if (conf.doProbe
        && prober
    ) {
        prober->get_stats().print_short(this, 0, 0);
        if (conf.do_print_times)
            print_stats_line("c probing time"
            , prober->get_stats().cpu_time
            , stats_line_percent(prober->get_stats().cpu_time, cpu_time)
            , "% time"
            );

        prober->get_stats().print_short(this, 0, 0);
    }
    //OccSimplifier stats
    if (conf.perform_occur_based_simp) {
        if (conf.do_print_times)
        print_stats_line("c OccSimplifier time"
            , occsimplifier->get_stats().total_time(occsimplifier)
            , stats_line_percent(occsimplifier->get_stats().total_time(occsimplifier) ,cpu_time)
            , "% time"
        );
        occsimplifier->get_stats().print_extra_times();
        occsimplifier->get_sub_str()->get_stats().print_short(this);
    }
    print_stats_line("c SCC time"
        , varReplacer->get_scc_finder()->get_stats().cpu_time
        , stats_line_percent(varReplacer->get_scc_finder()->get_stats().cpu_time, cpu_time)
        , "% time"
    );
    varReplacer->get_scc_finder()->get_stats().print_short(NULL);
    varReplacer->print_some_stats(cpu_time);

    //varReplacer->get_stats().print_short(nVars());
    print_stats_line("c distill time"
                    , distill_long_cls->get_stats().time_used
                    , stats_line_percent(distill_long_cls->get_stats().time_used, cpu_time)
                    , "% time"
    );
    print_stats_line("c strength cache-irred time"
                    , dist_long_with_impl->get_stats().irredCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().irredCacheBased.cpu_time, cpu_time)
                    , "% time"
    );
    print_stats_line("c strength cache-red time"
                    , dist_long_with_impl->get_stats().redCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().redCacheBased.cpu_time, cpu_time)
                    , "% time"
    );
    if (conf.doCache) {
        implCache.print_statsSort(this);
    }

    if (conf.do_print_times) {
        print_stats_line("c Conflicts in UIP"
            , sumConflicts
            , float_div(sumConflicts, cpu_time)
            , "confl/time_this_thread"
        );
    } else {
        print_stats_line("c Conflicts in UIP", sumConflicts);
    }
    double vm_usage;
    print_stats_line("c Mem used"
        , (double)memUsedTotal(vm_usage)/(1024UL*1024UL)
        , "MB"
    );
    print_stats_time(cpu_time, cpu_time_total);
}

void Solver::print_full_restart_stat(const double cpu_time, const double cpu_time_total) const
{
    cout << "c All times are for this thread only except if explicity specified" << endl;
    sumSearchStats.print(sumPropStats.propagations, conf.do_print_times);
    sumPropStats.print(sumSearchStats.cpu_time);
    print_stats_line("c props/decision"
        , float_div(propStats.propagations, sumSearchStats.decisions)
    );
    print_stats_line("c props/conflict"
        , float_div(propStats.propagations, sumConflicts)
    );
    cout << "c ------- FINAL TOTAL SOLVING STATS END ---------" << endl;
    //reduceDB->get_total_time().print(cpu_time);

    print_stats_line("c 0-depth assigns", trail.size()
        , stats_line_percent(trail.size(), nVarsOuter())
        , "% vars"
    );
    print_stats_line("c 0-depth assigns by CNF"
        , zeroLevAssignsByCNF
        , stats_line_percent(zeroLevAssignsByCNF, nVarsOutside())
        , "% vars"
    );

    //Failed lit stats
    if (conf.doProbe) {
        if (conf.do_print_times)
            print_stats_line("c probing time"
            , prober->get_stats().cpu_time
            , stats_line_percent(prober->get_stats().cpu_time, cpu_time)
            , "% time"
            );

        prober->get_stats().print(nVarsOuter(), conf.do_print_times);
    }

    //OccSimplifier stats
    if (conf.perform_occur_based_simp) {
        if (conf.do_print_times)
            print_stats_line("c OccSimplifier time"
            , occsimplifier->get_stats().total_time(occsimplifier)
            , stats_line_percent(occsimplifier->get_stats().total_time(occsimplifier), cpu_time)
            , "% time"
            );

        occsimplifier->get_stats().print(nVarsOuter(), occsimplifier);
        occsimplifier->get_sub_str()->get_stats().print();
    }

    //TODO after TRI to LONG conversion
    /*if (occsimplifier && conf.doGateFind) {
        occsimplifier->print_gatefinder_stats();
    }*/

    //VarReplacer stats
    if (conf.do_print_times)
        print_stats_line("c SCC time"
        , varReplacer->get_scc_finder()->get_stats().cpu_time
        , stats_line_percent(varReplacer->get_scc_finder()->get_stats().cpu_time, cpu_time)
        , "% time"
        );
    varReplacer->get_scc_finder()->get_stats().print();

    varReplacer->get_stats().print(nVarsOuter());
    varReplacer->print_some_stats(cpu_time);

    //DistillerAllWithAll stats
    if (conf.do_print_times)
        print_stats_line("c distill time"
                    , distill_long_cls->get_stats().time_used
                    , stats_line_percent(distill_long_cls->get_stats().time_used, cpu_time)
                    , "% time");
    distill_long_cls->get_stats().print(nVarsOuter());

    if (conf.do_print_times)
        print_stats_line("c strength cache-irred time"
                    , dist_long_with_impl->get_stats().irredCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().irredCacheBased.cpu_time, cpu_time)
                    , "% time");
    if (conf.do_print_times)
        print_stats_line("c strength cache-red time"
                    , dist_long_with_impl->get_stats().redCacheBased.cpu_time
                    , stats_line_percent(dist_long_with_impl->get_stats().redCacheBased.cpu_time, cpu_time)
                    , "% time");
    dist_long_with_impl->get_stats().print();

    if (conf.doStrSubImplicit) {
        subsumeImplicit->get_stats().print("");
    }

    if (conf.doCache) {
        implCache.print_stats(this);
    }

    //Other stats
    if (conf.do_print_times) {
        print_stats_line("c Conflicts in UIP"
            , sumConflicts
            , float_div(sumConflicts, cpu_time)
            , "confl/time_this_thread"
        );
    } else {
        print_stats_line("c Conflicts in UIP", sumConflicts);
    }
    print_stats_time(cpu_time, cpu_time_total);
    print_mem_stats();
}

uint64_t Solver::print_watch_mem_used(const uint64_t rss_mem_used) const
{
    size_t alloc = watches.mem_used_alloc();
    print_stats_line("c Mem for watch alloc"
        , alloc/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(alloc, rss_mem_used)
        , "%"
    );

    size_t array = watches.mem_used_array();
    print_stats_line("c Mem for watch array"
        , array/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(array, rss_mem_used)
        , "%"
    );

    return alloc + array;
}

size_t Solver::mem_used() const
{
    size_t mem = 0;
    mem += Searcher::mem_used();
    mem += outside_assumptions.capacity()*sizeof(Lit);

    return mem;
}

uint64_t Solver::mem_used_vardata() const
{
    uint64_t mem = 0;
    mem += assigns.capacity()*sizeof(lbool);
    mem += varData.capacity()*sizeof(VarData);

    return mem;
}

void Solver::print_mem_stats() const
{
    double vm_mem_used = 0;
    const uint64_t rss_mem_used = memUsedTotal(vm_mem_used);
    print_stats_line("c Mem used"
        , rss_mem_used/(1024UL*1024UL)
        , "MB"
    );
    uint64_t account = 0;

    account += print_mem_used_longclauses(rss_mem_used);
    account += print_watch_mem_used(rss_mem_used);

    size_t mem = 0;
    mem += mem_used_vardata();
    print_stats_line("c Mem for assings&vardata"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    mem = implCache.mem_used();
    print_stats_line("c Mem for implication cache"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    account += print_stamp_mem(rss_mem_used);

    mem = mem_used();
    print_stats_line("c Mem for search&solve"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    mem = CNF::mem_used_renumberer();
    print_stats_line("c Mem for renumberer"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    if (occsimplifier) {
        mem = occsimplifier->mem_used();
        print_stats_line("c Mem for occsimplifier"
            , mem/(1024UL*1024UL)
            , "MB"
            , stats_line_percent(mem, rss_mem_used)
            , "%"
        );
        account += mem;

        mem = occsimplifier->mem_used_xor();
        print_stats_line("c Mem for xor-finder"
            , mem/(1024UL*1024UL)
            , "MB"
            , stats_line_percent(mem, rss_mem_used)
            , "%"
        );
        account += mem;
    }

    mem = varReplacer->mem_used();
    print_stats_line("c Mem for varReplacer&SCC"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    if (subsumeImplicit) {
        mem = subsumeImplicit->mem_used();
        print_stats_line("c Mem for impl subsume"
            , mem/(1024UL*1024UL)
            , "MB"
            , stats_line_percent(mem, rss_mem_used)
            , "%"
        );
        account += mem;
    }


    mem = distill_long_cls->mem_used();
    mem += dist_long_with_impl->mem_used();
    mem += dist_impl_with_impl->mem_used();
    print_stats_line("c Mem for 3 distills"
        , mem/(1024UL*1024UL)
        , "MB"
        , stats_line_percent(mem, rss_mem_used)
        , "%"
    );
    account += mem;

    if (prober) {
        mem = prober->mem_used() + intree->mem_used();
        print_stats_line("c Mem for prober+intree"
            , mem/(1024UL*1024UL)
            , "MB"
            , stats_line_percent(mem, rss_mem_used)
            , "%"
        );
        account += mem;
    }

    print_stats_line("c Accounted for mem (rss)"
        , stats_line_percent(account, rss_mem_used)
        , "%"
    );
    print_stats_line("c Accounted for mem (vm)"
        , stats_line_percent(account, vm_mem_used)
        , "%"
    );
}

void Solver::print_clause_size_distrib()
{
    size_t size3 = 0;
    size_t size4 = 0;
    size_t size5 = 0;
    size_t sizeLarge = 0;
    for(vector<ClOffset>::const_iterator
        it = longIrredCls.begin(), end = longIrredCls.end()
        ; it != end
        ; ++it
    ) {
        Clause* cl = cl_alloc.ptr(*it);
        switch(cl->size()) {
            case 0:
            case 1:
            case 2:
                assert(false);
                break;
            case 3:
                size3++;
                break;
            case 4:
                size4++;
                break;
            case 5:
                size5++;
                break;
            default:
                sizeLarge++;
                break;
        }
    }

    cout
    << "c clause size stats."
    << " size3: " << size3
    << " size4: " << size4
    << " size5: " << size5
    << " larger: " << sizeLarge << endl;
}


vector<Lit> Solver::get_zero_assigned_lits(const bool backnumber,
                                           const bool only_nvars) const
{
    vector<Lit> lits;
    assert(decisionLevel() == 0);
    size_t until;
    if (only_nvars) {
        until = nVars();
    } else {
        until = assigns.size();
    }
    for(size_t i = 0; i < until; i++) {
        if (assigns[i] != l_Undef) {
            Lit lit(i, assigns[i] == l_False);

            //Update to higher-up
            lit = varReplacer->get_lit_replaced_with(lit);
            if (varData[lit.var()].is_bva == false) {
                if (backnumber) {
                    lits.push_back(map_inter_to_outer(lit));
                } else {
                    lits.push_back(lit);
                }

            }

            //Everything it repaces has also been set
            const vector<uint32_t> vars = varReplacer->get_vars_replacing(lit.var());
            for(const uint32_t var: vars) {
                if (varData[var].is_bva)
                    continue;

                Lit tmp_lit = Lit(var, false);
                assert(varReplacer->get_lit_replaced_with(tmp_lit).var() == lit.var());
                if (lit != varReplacer->get_lit_replaced_with(tmp_lit)) {
                    tmp_lit ^= true;
                }
                assert(lit == varReplacer->get_lit_replaced_with(tmp_lit));

                if (backnumber) {
                    lits.push_back(map_inter_to_outer(tmp_lit));
                } else {
                    lits.push_back(tmp_lit);
                }
            }
        }
    }

    //Remove duplicates. Because of above replacing-mimicing algo
    //multipe occurrences of literals can be inside
    std::sort(lits.begin(), lits.end());
    vector<Lit>::iterator it = std::unique (lits.begin(), lits.end());
    lits.resize( std::distance(lits.begin(),it) );

    //Update to outer without BVA
    if (backnumber) {
        vector<uint32_t> my_map = build_outer_to_without_bva_map();
        updateLitsMap(lits, my_map);
        for(const Lit lit: lits) {
            assert(lit.var() < nVarsOutside());
        }
    }

    return lits;
}

bool Solver::verify_model_implicit_clauses() const
{
    uint32_t wsLit = 0;
    for (watch_array::const_iterator
        it = watches.begin(), end = watches.end()
        ; it != end
        ; ++it, wsLit++
    ) {
        Lit lit = Lit::toLit(wsLit);
        watch_subarray_const ws = *it;

        for (Watched w: ws) {
            if (w.isBin()
                && model_value(lit) != l_True
                && model_value(w.lit2()) != l_True
            ) {
                cout
                << "bin clause: "
                << lit << " , " << w.lit2()
                << " not satisfied!"
                << endl;

                cout
                << "value of unsat bin clause: "
                << value(lit) << " , " << value(w.lit2())
                << endl;

                return false;
            }
        }
    }

    return true;
}

bool Solver::verify_model_long_clauses(const vector<ClOffset>& cs) const
{
    #ifdef VERBOSE_DEBUG
    cout << "Checking clauses whether they have been properly satisfied." << endl;
    #endif

    bool verificationOK = true;

    for (vector<ClOffset>::const_iterator
        it = cs.begin(), end = cs.end()
        ; it != end
        ; ++it
    ) {
        Clause& cl = *cl_alloc.ptr(*it);
        for (uint32_t j = 0; j < cl.size(); j++)
            if (model_value(cl[j]) == l_True)
                goto next;

        cout << "unsatisfied clause: " << cl << endl;
        verificationOK = false;
        next:
        ;
    }

    return verificationOK;
}

bool Solver::verify_model() const
{
    bool verificationOK = true;
    verificationOK &= verify_model_long_clauses(longIrredCls);
    for(auto& lredcls: longRedCls) {
        verificationOK &= verify_model_long_clauses(lredcls);
    }
    verificationOK &= verify_model_implicit_clauses();

    if (conf.verbosity && verificationOK) {
        cout
        << "c Verified "
        << longIrredCls.size() + longRedCls.size()
            + binTri.irredBins + binTri.redBins
        << " clause(s)."
        << endl;
    }

    return verificationOK;
}

size_t Solver::get_num_nonfree_vars() const
{
    size_t nonfree = 0;
    if (decisionLevel() == 0) {
        nonfree += trail.size();
    } else {
        nonfree += trail_lim[0];
    }

    if (occsimplifier) {
        if (conf.perform_occur_based_simp) {
            nonfree += occsimplifier->get_num_elimed_vars();
        }
    }
    nonfree += varReplacer->get_num_replaced_vars();
    return nonfree;
}

size_t Solver::get_num_free_vars() const
{
    return nVarsOuter() - get_num_nonfree_vars();
}

void Solver::print_clause_stats() const
{
    //Irredundant
    cout << " " << print_value_kilo_mega(longIrredCls.size());
    cout << " " << print_value_kilo_mega(binTri.irredBins);
    cout
    << " " << std::setw(7) << std::fixed << std::setprecision(2)
    << ratio_for_stat(litStats.irredLits, longIrredCls.size())
    << " " << std::setw(7) << std::fixed << std::setprecision(2)
    << ratio_for_stat(litStats.irredLits + binTri.irredBins*2
    , longIrredCls.size() + binTri.irredBins)
    ;

    //Redundant
    size_t tot = 0;
    for(auto& lredcls: longRedCls) {
        cout << " " << print_value_kilo_mega(lredcls.size());
        tot += lredcls.size();
    }

    cout << " " << print_value_kilo_mega(binTri.redBins);
    cout
    << " " << std::setw(7) << std::fixed << std::setprecision(2)
    << ratio_for_stat(litStats.redLits, tot)
    << " " << std::setw(7) << std::fixed << std::setprecision(2)
    << ratio_for_stat(litStats.redLits + binTri.redBins*2
    , tot + binTri.redBins)
    ;
}

const char* Solver::get_version_sha1()
{
    return CMSGen::get_version_sha1();
}

const char* Solver::get_version_tag()
{
    return CMSGen::get_version_tag();
}

const char* Solver::get_compilation_env()
{
    return CMSGen::get_compilation_env();
}

void Solver::print_watch_list(watch_subarray_const ws, const Lit lit) const
{
    for (const Watched *it = ws.begin(), *end = ws.end()
        ; it != end
        ; ++it
    ) {
        if (it->isClause()) {
            cout
            << "Clause: " << *cl_alloc.ptr(it->get_offset());
        }

        if (it->isBin()) {
            cout
            << "BIN: " << lit << ", " << it->lit2()
            << " (l: " << it->red() << ")";
        }

        cout << endl;
    }
    cout << endl;
}

void Solver::check_implicit_propagated() const
{
    size_t wsLit = 0;
    for(watch_array::const_iterator
        it = watches.begin(), end = watches.end()
        ; it != end
        ; ++it, wsLit++
    ) {
        const Lit lit = Lit::toLit(wsLit);
        watch_subarray_const ws = *it;
        for(const Watched *it2 = ws.begin(), *end2 = ws.end()
            ; it2 != end2
            ; it2++
        ) {
            //Satisfied, or not implicit, skip
            if (value(lit) == l_True
                || it2->isClause()
            ) {
                continue;
            }

            const lbool val1 = value(lit);
            const lbool val2 = value(it2->lit2());

            //Handle binary
            if (it2->isBin()) {
                if (val1 == l_False) {
                    if (val2 != l_True) {
                        cout << "not prop BIN: "
                        << lit << ", " << it2->lit2()
                        << " (red: " << it2->red()
                        << endl;
                    }
                    assert(val2 == l_True);
                }

                if (val2 == l_False)
                    assert(val1 == l_True);
            }
        }
    }
}

size_t Solver::get_num_vars_elimed() const
{
    if (conf.perform_occur_based_simp) {
        return occsimplifier->get_num_elimed_vars();
    } else {
        return 0;
    }
}

void Solver::free_unused_watches()
{
    size_t wsLit = 0;
    for (watch_array::iterator
        it = watches.begin(), end = watches.end()
        ; it != end
        ; ++it, wsLit++
    ) {
        Lit lit = Lit::toLit(wsLit);
        if (varData[lit.var()].removed == Removed::elimed
            || varData[lit.var()].removed == Removed::replaced
        ) {
            watch_subarray ws = *it;
            assert(ws.empty());
            ws.clear();
        }
    }

    if ((sumConflicts - last_full_watch_consolidate) > conf.full_watch_consolidate_every_n_confl) {
        last_full_watch_consolidate = sumConflicts;
        consolidate_watches(true);
    } else {
        consolidate_watches(false);
    }
}

bool Solver::fully_enqueue_these(const vector<Lit>& toEnqueue)
{
    assert(ok);
    assert(decisionLevel() == 0);
    for(const Lit lit: toEnqueue) {
        if (!fully_enqueue_this(lit)) {
            return false;
        }
    }

    return true;
}

bool Solver::fully_enqueue_this(const Lit lit)
{
    const lbool val = value(lit);
    if (val == l_Undef) {
        assert(varData[lit.var()].removed == Removed::none);
        enqueue(lit);
        ok = propagate<true>().isNULL();

        if (!ok) {
            return false;
        }
    } else if (val == l_False) {
        ok = false;
        return false;
    }
    return true;
}

void Solver::new_external_var()
{
    new_var(false);
}

void Solver::new_external_vars(size_t n)
{
    new_vars(n);
}

void Solver::add_in_partial_solving_stats()
{
    Searcher::add_in_partial_solving_stats();
    sumSearchStats += Searcher::get_stats();
    sumPropStats += propStats;
}

bool Solver::add_clause_outer(const vector<Lit>& lits, bool red)
{
    if (!ok) {
        return false;
    }
    #ifdef SLOW_DEBUG //we check for this during back-numbering
    check_too_large_variable_number(lits);
    #endif
    back_number_from_outside_to_outer(lits);
    return addClauseInt(back_number_from_outside_to_outer_tmp, red);
}

bool Solver::add_xor_clause_outer(const vector<uint32_t>& vars, bool rhs)
{
    if (!ok) {
        return false;
    }

    vector<Lit> lits(vars.size());
    for(size_t i = 0; i < vars.size(); i++) {
        lits[i] = Lit(vars[i], false);
    }
    #ifdef SLOW_DEBUG //we check for this during back-numbering
    check_too_large_variable_number(lits);
    #endif

    back_number_from_outside_to_outer(lits);
    addClauseHelper(back_number_from_outside_to_outer_tmp);
    add_xor_clause_inter(back_number_from_outside_to_outer_tmp, rhs, true, false);

    return ok;
}

void Solver::check_too_large_variable_number(const vector<Lit>& lits) const
{
    for (const Lit lit: lits) {
        if (lit.var() >= nVarsOutside()) {
            std::cerr
            << "ERROR: Variable " << lit.var() + 1
            << " inserted, but max var is "
            << nVarsOutside()
            << endl;
            assert(false);
            std::exit(-1);
        }
        release_assert(lit.var() < nVarsOutside()
        && "Clause inserted, but variable inside has not been declared with PropEngine::new_var() !");

        if (lit.var() >= var_Undef) {
            std::cerr << "ERROR: Variable number " << lit.var()
            << "too large. PropBy is limiting us, sorry" << endl;
            assert(false);
            std::exit(-1);
        }
    }
}

vector<pair<Lit, Lit> > Solver::get_all_binary_xors() const
{
    vector<pair<Lit, Lit> > bin_xors = varReplacer->get_all_binary_xors_outer();

    //Update to outer without BVA
    vector<pair<Lit, Lit> > ret;
    const vector<uint32_t> my_map = build_outer_to_without_bva_map();
    for(std::pair<Lit, Lit> p: bin_xors) {
        if (p.first.var() < my_map.size()
            && p.second.var() < my_map.size()
        ) {
            ret.push_back(std::make_pair(
                getUpdatedLit(p.first, my_map)
                , getUpdatedLit(p.second, my_map)
            ));
        }
    }

    for(const std::pair<Lit, Lit>& val: ret) {
        assert(val.first.var() < nVarsOutside());
        assert(val.second.var() < nVarsOutside());
    }

    return ret;
}

void Solver::update_assumptions_after_varreplace()
{
    #ifdef SLOW_DEBUG
    for(AssumptionPair& lit_pair: assumptions) {
        const Lit inter_lit = map_outer_to_inter(lit_pair.lit_outer);
        assert(inter_lit.var() < varData.size());
        if (varData[inter_lit.var()].assumption == l_Undef) {
            cout << "Assump " << inter_lit << " has .assumption : "
            << varData[inter_lit.var()].assumption << endl;
        }
        assert(varData[inter_lit.var()].assumption != l_Undef);
    }
    #endif

    //Update assumptions
    for(AssumptionPair& lit_pair: assumptions) {
        const Lit orig = lit_pair.lit_outer;
        lit_pair.lit_outer = varReplacer->get_lit_replaced_with_outer(orig);

        //remove old from set + add new to set
        if (orig != lit_pair.lit_outer) {
            const Lit old_inter_lit = map_outer_to_inter(orig);
            const Lit new_inter_lit = map_outer_to_inter(lit_pair.lit_outer);
            varData[old_inter_lit.var()].assumption = l_Undef;
            varData[new_inter_lit.var()].assumption =
                new_inter_lit.sign() ? l_False: l_True;
        }
    }

    #ifdef SLOW_DEBUG
    check_assumptions_sanity();
    #endif
}

//TODO later, this can be removed, get_num_free_vars() is MUCH cheaper to
//compute but may have some bugs here-and-there
uint32_t Solver::num_active_vars() const
{
    uint32_t numActive = 0;
    uint32_t removed_replaced = 0;
    uint32_t removed_set = 0;
    uint32_t removed_elimed = 0;
    uint32_t removed_non_decision = 0;
    for(uint32_t var = 0; var < nVarsOuter(); var++) {
        if (value(var) != l_Undef) {
            if (varData[var].removed != Removed::none)
            {
                cout << "ERROR: var " << var + 1 << " has removed: "
                << removed_type_to_string(varData[var].removed)
                << " but is set to " << value(var) << endl;
                assert(varData[var].removed == Removed::none);
                exit(-1);
            }
            removed_set++;
            continue;
        }
        switch(varData[var].removed) {
            case Removed::elimed :
                removed_elimed++;
                continue;
            case Removed::replaced:
                removed_replaced++;
                continue;
            case Removed::none:
                break;
        }
        if (varData[var].removed != Removed::none) {
            removed_non_decision++;
        }
        numActive++;
    }
    assert(removed_non_decision == 0);
    if (occsimplifier) {
        assert(removed_elimed == occsimplifier->get_num_elimed_vars());
    } else {
        assert(removed_elimed == 0);
    }

    assert(removed_set == ((decisionLevel() == 0) ? trail.size() : trail_lim[0]));

    assert(removed_replaced == varReplacer->get_num_replaced_vars());
    assert(numActive == get_num_free_vars());

    return numActive;
}

lbool Solver::load_solution_from_file(const string& fname)
{
    //At this point, model is set up, we just need to fill the l_Undef in
    //from assigns
    lbool status = l_Undef;
    FILE* input_stream = fopen(fname.c_str(), "r");
    if (input_stream == NULL) {
        std::cerr << "ERROR: could not open solution file "
        << fname
        << endl;
        std::exit(-1);
    }
    StreamBuffer<FILE*, FN> in(input_stream);

    unsigned lineNum = 0;
    std::string str;
    bool sol_already_seen = false;
    for (;;) {
        in.skipWhitespace();
        switch (*in) {
            case EOF:
                goto end;
            case 's': {
                if (sol_already_seen) {
                    std::cerr << "ERROR: The input file you gave for solution extension contains more than one line starting with 's', which indicates more than one solution! That is not supported!" << endl;
                    exit(-1);
                }
                sol_already_seen = true;
                ++in;
                in.skipWhitespace();
                in.parseString(str);
                if (str == "SATISFIABLE") {
                    status = l_True;
                } else if (str == "UNSATISFIABLE") {
                    status = l_False;
                    goto end;
                } else if (str == "INDETERMINATE") {
                    std::cerr << "The solution given for preproc extension is INDETERMINATE -- we cannot extend it!" << endl;
                    exit(-1);
                } else {
                    std::cerr << "ERROR: Cannot parse solution line starting with 's'"
                    << endl;
                    std::exit(-1);
                }
                in.skipLine();
                lineNum++;
                break;
            }
            case 'v': {
                if (status == l_False) {
                    std::cerr << "ERROR: The solution you gave is UNSAT but it has 'v' lines. This is definietely wrong." << endl;
                    exit(-1);
                }
                ++in;
                parse_v_line(&in, lineNum);
                in.skipLine();
                lineNum++;
                break;
            }
            case '\n':
                std::cerr
                << "c WARNING: Empty line at line number " << lineNum+1
                << " -- this is not part of the DIMACS specifications. Ignoring."
                << endl;
                in.skipLine();
                lineNum++;
                break;
            default:
                in.skipLine();
                lineNum++;
                break;
        }
    }

    end:
    fclose(input_stream);
    return status;
}

template<typename A>
void Solver::parse_v_line(A* in, const size_t lineNum)
{
    model.resize(nVarsOuter(), l_Undef);

    int32_t parsed_lit;
    uint32_t var;
    for (;;) {
        if (!in->parseInt(parsed_lit, lineNum, true)) {
            exit(-1);
        }
        if (parsed_lit == std::numeric_limits<int32_t>::max()) {
            break;
        }
        if (parsed_lit == 0) break;
        var = abs(parsed_lit)-1;
        if (var >= nVars()
            || var >= model.size()
            || var >= varData.size()
        ) {
            std::cerr
            << "ERROR! "
            << "Variable in solution is too large: " << var +1 << endl
            << "--> At line " << lineNum+1
            << endl;
            std::exit(-1);
        }

        //Don't overwrite previously computed values
        if (model[var] == l_Undef
            && varData[var].removed == Removed::none
        ) {
            model[var] = parsed_lit < 0 ? l_False : l_True;
            if (conf.verbosity >= 10) {
                uint32_t outer_var = map_inter_to_outer(var);
                cout << "Read V line: model for inter var " << (var+1)
                << " (outer ver for this is: " << outer_var+1 << ")"
                << " set to " << model[var] << endl;
            }
        }
    }
}


void Solver::check_implicit_stats(const bool onlypairs) const
{
    //Don't check if in crazy mode
    #ifdef NDEBUG
    return;
    #endif

    //Check number of red & irred binary clauses
    uint64_t thisNumRedBins = 0;
    uint64_t thisNumIrredBins = 0;

    size_t wsLit = 0;
    for(watch_array::const_iterator
        it = watches.begin(), end = watches.end()
        ; it != end
        ; ++it, wsLit++
    ) {
        watch_subarray_const ws = *it;
        for(const Watched* it2 = ws.begin(), *end2 = ws.end()
            ; it2 != end2
            ; it2++
        ) {
            if (it2->isBin()) {
                #ifdef DEBUG_IMPLICIT_PAIRS_TRIPLETS
                Lit lits[2];
                lits[0] = Lit::toLit(wsLit);
                lits[1] = it2->lit2();
                std::sort(lits, lits + 2);
                findWatchedOfBin(watches, lits[0], lits[1], it2->red());
                findWatchedOfBin(watches, lits[1], lits[0], it2->red());
                #endif

                if (it2->red())
                    thisNumRedBins++;
                else
                    thisNumIrredBins++;

                continue;
            }
        }
    }

    if (onlypairs) {
        goto end;
    }

    if (thisNumIrredBins/2 != binTri.irredBins) {
        std::cerr
        << "ERROR:"
        << " thisNumIrredBins/2: " << thisNumIrredBins/2
        << " thisNumIrredBins: " << thisNumIrredBins
        << " binTri.irredBins: " << binTri.irredBins
        << endl;
    }
    assert(thisNumIrredBins % 2 == 0);
    assert(thisNumIrredBins/2 == binTri.irredBins);

    if (thisNumRedBins/2 != binTri.redBins) {
        std::cerr
        << "ERROR:"
        << " thisNumRedBins/2: " << thisNumRedBins/2
        << " thisNumRedBins: " << thisNumRedBins
        << " binTri.redBins: " << binTri.redBins
        << endl;
    }
    assert(thisNumRedBins % 2 == 0);
    assert(thisNumRedBins/2 == binTri.redBins);

    end:;
}

void Solver::check_stats(const bool allowFreed) const
{
    //If in crazy mode, don't check
    #ifdef NDEBUG
    return;
    #endif

    check_implicit_stats();

    uint64_t numLitsIrred = count_lits(longIrredCls, false, allowFreed);
    if (numLitsIrred != litStats.irredLits) {
        std::cerr << "ERROR: " << endl
        << "->numLitsIrred: " << numLitsIrred << endl
        << "->litStats.irredLits: " << litStats.irredLits << endl;
    }

    uint64_t numLitsRed = 0;
    for(auto& lredcls: longRedCls) {
        numLitsRed += count_lits(lredcls, true, allowFreed);
    }
    if (numLitsRed != litStats.redLits) {
        std::cerr << "ERROR: " << endl
        << "->numLitsRed: " << numLitsRed << endl
        << "->litStats.redLits: " << litStats.redLits << endl;
    }
    assert(numLitsRed == litStats.redLits);
    assert(numLitsIrred == litStats.irredLits);
}

vector<Lit> Solver::get_toplevel_units_internal(bool outer_numbering) const
{
    assert(!outer_numbering);
    vector<Lit> units;
    for(size_t i = 0; i < nVars(); i++) {
        if (value(i) != l_Undef) {
            Lit l = Lit(i, value(i) == l_False);
            units.push_back(l);
        }
    }

    return units;
}

vector<Xor> Solver::get_recovered_xors(bool elongate)
{
    vector<Xor> xors_ret;
    if (elongate && solver->okay()) {
        XorFinder finder(NULL, this);
        auto xors = xorclauses;

        //YEP -- the solver state can turn to OK=false
        finder.xor_together_xors(xors);
        //YEP -- the solver state can turn to OK=false
        if (solver->okay()) {
            finder.add_new_truths_from_xors(xors);
        }
        //YEP -- the solver state can turn to OK=false

        renumber_xors_to_outside(xors, xors_ret);
        return xors_ret;
    } else {
        renumber_xors_to_outside(xorclauses, xors_ret);
        return xors_ret;
    }
}

void Solver::renumber_xors_to_outside(const vector<Xor>& xors, vector<Xor>& xors_ret)
{
    const vector<uint32_t> outer_to_without_bva_map = solver->build_outer_to_without_bva_map();

    if (conf.verbosity >= 5) {
        cout << "XORs before outside numbering:" << endl;
        for(auto& x: xors) {
            cout << x << endl;
        }
    }

    for(auto& x: xors) {
        bool OK = true;
        for(const auto v: x.get_vars()) {
            if (varData[v].is_bva) {
                OK = false;
                break;
            }
        }
        if (!OK) {
            continue;
        }

        vector<uint32_t> t = xor_outer_numbered(x.get_vars());
        for(auto& v: t) {
            v = outer_to_without_bva_map[v];
        }
        xors_ret.push_back(Xor(t, x.rhs));
    }
}

#ifdef USE_GAUSS
bool Solver::init_all_matrices()
{
    assert(ok);
    for (EGaussian*& g :gmatrices) {
        bool created = false;
        // initial arrary. return true is fine , return false means solver already false;
        if (!g->full_init(created)) {
            return false;
        }
        if (!ok) {
            break;
        }
        if (!created) {
            delete g;
            if (conf.verbosity > 5) {
                cout << "DELETED matrix" << endl;
            }
            g = NULL;
        }
    }
    for(auto& gqd: gqueuedata) {
        gqd.reset_stats();
    }
    xor_clauses_updated = false;
    return solver->okay();
}
#endif //USE_GAUSS


void Solver::start_getting_small_clauses(const uint32_t max_len, const uint32_t max_glue)
{
    if (!ok) {
        std::cerr << "ERROR: the system is in UNSAT state, learnt clauses are meaningless!" <<endl;
        exit(-1);
    }
    if (!learnt_clause_query_outer_to_without_bva_map.empty()) {
        std::cerr << "ERROR: You forgot to call end_getting_small_clauses() last time!" <<endl;
        exit(-1);
    }

    assert(learnt_clause_query_at == std::numeric_limits<uint32_t>::max());
    assert(learnt_clause_query_watched_at == std::numeric_limits<uint32_t>::max());
    assert(learnt_clause_query_watched_at_sub == std::numeric_limits<uint32_t>::max());
    assert(max_len >= 2);

    learnt_clause_query_at = 0;
    learnt_clause_query_watched_at = 0;
    learnt_clause_query_watched_at_sub = 0;
    learnt_clause_query_max_len = max_len;
    learnt_clause_query_max_glue = max_glue;
    learnt_clause_query_outer_to_without_bva_map = solver->build_outer_to_without_bva_map();
}

bool Solver::get_next_small_clause(vector<Lit>& out)
{
    assert(ok);

    while(learnt_clause_query_watched_at < solver->nVars()*2) {
        Lit l = Lit::toLit(learnt_clause_query_watched_at);
        watch_subarray_const ws = watches[l];
        while(learnt_clause_query_watched_at_sub < ws.size()) {
            const Watched& w = ws[learnt_clause_query_watched_at_sub];
            if (w.isBin() && w.lit2() < l && w.red()) {
                out.clear();
                out.push_back(l);
                out.push_back(w.lit2());
                out = clause_outer_numbered(out);
                if (all_vars_outside(out)) {
                    learnt_clausee_query_map_without_bva(out);
                    learnt_clause_query_watched_at_sub++;
                    return true;
                }
            }
            learnt_clause_query_watched_at_sub++;
        }
        learnt_clause_query_watched_at++;
        learnt_clause_query_watched_at_sub = 0;
    }

    while(learnt_clause_query_at < longRedCls[0].size()) {
        const ClOffset offs = longRedCls[0][learnt_clause_query_at];
        const Clause* cl = cl_alloc.ptr(offs);
        if (cl->size() <= learnt_clause_query_max_len
            && cl->stats.glue <= learnt_clause_query_max_glue
        ) {
            out = clause_outer_numbered(*cl);
            if (all_vars_outside(out)) {
                learnt_clausee_query_map_without_bva(out);
                learnt_clause_query_at++;
                return true;
            }
        }
        learnt_clause_query_at++;
    }

    assert(learnt_clause_query_at >= longRedCls[0].size());
    uint32_t at_lev1 = learnt_clause_query_at-longRedCls[0].size();
    while(at_lev1 < longRedCls[1].size()) {
        const ClOffset offs = longRedCls[1][at_lev1];
        const Clause* cl = cl_alloc.ptr(offs);
        if (cl->size() <= learnt_clause_query_max_len) {
            out = clause_outer_numbered(*cl);
            if (all_vars_outside(out)) {
                learnt_clausee_query_map_without_bva(out);
                learnt_clause_query_at++;
                return true;
            }
        }
        learnt_clause_query_at++;
        at_lev1++;
    }
    return false;
}

void Solver::end_getting_small_clauses()
{
    if (!ok) {
        std::cerr << "ERROR: the system is in UNSAT state, learnt clauses are meaningless!" <<endl;
        exit(-1);
    }

    learnt_clause_query_at = std::numeric_limits<uint32_t>::max();
    learnt_clause_query_watched_at = std::numeric_limits<uint32_t>::max();
    learnt_clause_query_watched_at_sub = std::numeric_limits<uint32_t>::max();
    learnt_clause_query_outer_to_without_bva_map.clear();
    learnt_clause_query_outer_to_without_bva_map.shrink_to_fit();
}

bool Solver::all_vars_outside(const vector<Lit>& cl) const
{
    for(const auto& l: cl) {
        if (varData[map_outer_to_inter(l.var())].is_bva)
            return false;
    }
    return true;
}

void Solver::learnt_clausee_query_map_without_bva(vector<Lit>& cl)
{
    for(auto& l: cl) {
        l = Lit(learnt_clause_query_outer_to_without_bva_map[l.var()], l.sign());
    }
}

void Solver::add_empty_cl_to_drat()
{
    *drat << add
    << fin;
    drat->flush();
}

void Solver::check_assigns_for_assumptions() const
{
    for (const auto& ass: solver->assumptions) {
        const Lit inter = map_outer_to_inter(ass.lit_outer);
        if (value(inter) != l_True) {
            cout << "ERROR: Internal assumption " << inter
            << " is not set to l_True, it's set to: " << value(inter)
            << endl;
            assert(lit_inside_assumptions(inter) == l_True);
        }
        assert(value(inter) == l_True);
    }
}

bool Solver::check_assumptions_contradict_foced_assignement() const
{
    for (auto& ass: solver->assumptions) {
        const Lit inter = map_outer_to_inter(ass.lit_outer);
        if (value(inter) == l_False) {
            return true;
        }
    }
    return false;
}

void Solver::set_var_weight(
const Lit lit, const double weight
) {
    if (lit.sign()) {
        cout << "ERROR: only positive literals can have weights."
            << " You gave weight '" << weight << " to literal: '" << (lit) << "'"
            << "NOTE: A weight of 0.7 for '-2' is the same as the weight of 0.3 for '2'" << endl;
        exit(-1);
    }
    if (weight < 0.0 || weight > 1.0) {
        cout << "ERROR: Weight must be between 0 and 1"
            << " You gave weight '" << weight << " to literal: '" << (lit) << "'"
            << endl;
        exit(-1);
    }
    varData[lit.var()].weight = weight;
}
