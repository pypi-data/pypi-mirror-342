/* * * * * * * * * * * * * * * * * * * *
 *  ZCurvePy Source Code               *
 *                                     *
 *  @author      Zhang ZT, Gao F       *
 *  @copyright   Copyright 2025 TUBIC  *
 *  @date        2025-02-25            *
 *  @version     1.5.11                *
 * * * * * * * * * * * * * * * * * * * */
#include "ZCurvePyCore.h"
#include "ZCurvePyAPIs.h"

/* Methods definition of _ZCurvePy module */
static PyMethodDef _ZCurvePy_methods[] = {
    {"shuffle", (PyCFunction) ZCurvePy_shuffle, METH_VARARGS|METH_KEYWORDS, NULL},
    {"decode", (PyCFunction) ZCurvePy_decode, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

/* Definition of _ZCurvePy module */
static struct PyModuleDef _ZCurvePyModule = {
    PyModuleDef_HEAD_INIT,
    "_ZCurvePy",
    NULL,
    -1,
    _ZCurvePy_methods
};

/* Init function of _ZCurvePy */
PyMODINIT_FUNC PyInit__ZCurvePy(void) {
    /* Import necessary third-party modules */
    PyObject *Bio_module = PyImport_ImportModule("Bio.SeqRecord");
    PyObject *json_module = PyImport_ImportModule("json");
    SeqRecord = PyObject_GetAttrString(Bio_module, "SeqRecord");
    Py_DECREF(Bio_module);
    Py_DECREF(json_module);

    /* Key for BatchZCurveEncoder to parse parameters */
    keyK = Py_BuildValue("s", "k");
    keyPhase = Py_BuildValue("s", "phase");
    keyFreq = Py_BuildValue("s", "freq");
    keyLocal = Py_BuildValue("s", "local");
    keyHyper = Py_BuildValue("s", "hyper_params");
    keyNJobs = Py_BuildValue("s", "n_jobs");

    /* Init the _ZCurvePy module object */
    if (
        PyType_Ready(&ZCurveEncoderType) < 0 ||
        PyType_Ready(&ZCurvePlotterType) < 0 ||
        PyType_Ready(&BatchZCurveEncoderType) < 0 ||
        PyType_Ready(&BatchZCurvePlotterType) < 0
    ) return NULL;
    _ZCurvePy = PyModule_Create(&_ZCurvePyModule);
    if (_ZCurvePy == NULL)
        return NULL;
    
    /* Load Python type objects to the module */
    Py_INCREF(&ZCurveEncoderType);
    Py_INCREF(&ZCurvePlotterType);
    Py_INCREF(&BatchZCurveEncoderType);
    Py_INCREF(&BatchZCurvePlotterType);

    if (!PyModule_AddObject(_ZCurvePy, "ZCurveEncoder", (PyObject *) &ZCurveEncoderType))
    if (!PyModule_AddObject(_ZCurvePy, "ZCurvePlotter", (PyObject *) &ZCurvePlotterType))
    if (!PyModule_AddObject(_ZCurvePy, "BatchZCurveEncoder", (PyObject *) &BatchZCurveEncoderType))
    if (!PyModule_AddObject(_ZCurvePy, "BatchZCurvePlotter", (PyObject *) &BatchZCurvePlotterType))
        return _ZCurvePy;

    Py_DECREF(&ZCurveEncoderType);
    Py_DECREF(&ZCurvePlotterType);
    Py_DECREF(&BatchZCurveEncoderType);
    Py_DECREF(&BatchZCurvePlotterType);
    Py_DECREF(_ZCurvePy);

    return NULL;
}