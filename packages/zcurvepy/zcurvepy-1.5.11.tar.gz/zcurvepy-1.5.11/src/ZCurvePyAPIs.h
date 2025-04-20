/* * * * * * * * * * * * * * * * * * * *
 *  ZCurvePy Source Code               *
 *                                     *
 *  @author      Zhang ZT, Gao F       *
 *  @copyright   Copyright 2025 TUBIC  *
 *  @date        2025-02-25            *
 *  @version     1.5.11                *
 * * * * * * * * * * * * * * * * * * * */

// Supported Python Version: >= 3.9
#ifndef ZCURVEPY_APIS
#define ZCURVEPY_APIS

#define PY_SSIZE_T_CLEAN

#include<thread>
#include<vector>
#include<random>
#include<algorithm>
#include<cstdio>

#include<Python.h>
#include<numpy/arrayobject.h>
#include"ZCurvePyCore.h"

/* Keyword 'k' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyK;
/* Keyword 'phase' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyPhase;
/* Keyword 'freq' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyFreq;
/* Keyword 'local' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyLocal;
/* Keyword 'hyper_params' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyHyper;
/* Keyword 'n_jobs' for ZCurvePy.BatchZCurveEncoder */
extern PyObject *keyNJobs;
/* ZCurvePy main module object*/
extern PyObject *_ZCurvePy;
/* Bio.SeqRecord.SeqRecord (BioPython) type object */
extern PyObject *SeqRecord;
/* Python Type Object ZCurveEncoder*/
extern PyTypeObject ZCurveEncoderType;
/* Python Type Object ZCurvePlotter*/
extern PyTypeObject ZCurvePlotterType;
/* Python Type Object BatchZCurveEncoder*/
extern PyTypeObject BatchZCurveEncoderType;
/* Python Type Object BatchZCurvePlotter*/
extern PyTypeObject BatchZCurvePlotterType;
#ifdef __cplusplus
extern "C" {
#endif
/* shuffle C/C++ API able to handle many-type Python objects, like str, Seq and SeqRecord */
PyObject *ZCurvePy_shuffle(PyObject *, PyObject *, PyObject *);
/* decoding Z-curves */
PyObject *ZCurvePy_decode(PyObject *, PyObject *, PyObject *);
#ifdef __cplusplus
}
#endif
#endif