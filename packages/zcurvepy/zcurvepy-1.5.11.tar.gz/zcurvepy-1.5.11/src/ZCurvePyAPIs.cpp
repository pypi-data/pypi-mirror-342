#include"ZCurvePyAPIs.h"

PyObject *keyK = nullptr;
PyObject *keyPhase = nullptr;
PyObject *keyNJobs = nullptr;
PyObject *_ZCurvePy = nullptr;
PyObject *keyHyper = nullptr;
PyObject *keyFreq = nullptr;
PyObject *keyLocal = nullptr;
PyObject *SeqRecord = nullptr;

/* Keyword list of APIs for non-phase Z-curve transform */
/* 
 * @param freq  : do Z-curve transform based on frequency or count
 * @param local : use local frequencized mode or not
 */
static char *kwListTrans[] = {"freq", "local", NULL};
/* Keyword list of APIs for phase Z-curve transform */
/* 
 * @param phase : phase count for doing phase-specific transform
 * @param freq  : do Z-curve transform based on frequency or count
 * @param local : use local frequencized mode or not
 */
static char *kwListPhaseTrans[] = {"phase", "freq", "local", NULL};
/* Keyword list of APIs for Z-curve plotter */
/*
 * @param window   : sliding window size for doing mean smoothing
 * @param return_n : should return the x-values of 2D-curve or not
 */
static char *kwListCurve[] = {"window", "return_n", NULL};
/* Keyword list of APIs for Z-curve plotter (dS curves) */
/*
 * @param window   : sliding window size for doing mean smoothing
 * @param return_n : should return the x-values of 2D-curve or not
 * @param only_m : only return max point location
 */
static char *kwListdSCurve[] = {"window", "return_n", "only_m", NULL};
/* Modes for BatchZCurvePlotter */
static char *plotterMode[] = {"accum", "profile", "tetra"};
/* 
 * Convert C++ float array to Numpy array.
 *
 * @param params  array to be converted to list
 * @param len     length of the array
 * @return        Python list object
 */

static void deleteFloatArray(PyObject *capsule) {
    float *array = static_cast<float*>(PyCapsule_GetPointer(capsule, "float_arr"));
    delete[] array;
}
static PyObject *toNumpyArray(float *params, int len) {
    import_array();
    /* PASS 2025-04-17 */
    npy_intp dims[] = { len };
    PyObject* np_array = PyArray_SimpleNewFromData(1, dims, NPY_FLOAT32, params);

    if (!np_array) {
        delete[] params;
        Py_RETURN_NONE;
    }

    PyObject* capsule = PyCapsule_New(params, "float_arr", deleteFloatArray);

    if (!capsule) {
        Py_DECREF(np_array);
        delete[] params;
        Py_RETURN_NONE;
    }

    if (PyArray_SetBaseObject(reinterpret_cast<PyArrayObject*>(np_array), capsule) == -1) {
        Py_DECREF(np_array);
        Py_DECREF(capsule);
        Py_RETURN_NONE;
    }
    
    return np_array;
}
static void deleteIntArray(PyObject *capsule) {
    float *array = static_cast<float*>(PyCapsule_GetPointer(capsule, "int_arr"));
    delete[] array;
}
static PyObject *genNumpyArange(int len) {
    import_array();
    int *int_arr = new int[len];
    for (int i = 0; i < len; i ++)
        int_arr[i] = i;

    npy_intp dims[] = { len };
    PyObject* np_array = PyArray_SimpleNewFromData(1, dims, NPY_INT32, int_arr);

    if (!np_array) {
        delete[] int_arr;
        Py_RETURN_NONE;
    }

    PyObject* capsule = PyCapsule_New(int_arr, "int_arr", deleteIntArray);

    if (!capsule) {
        Py_DECREF(np_array);
        delete[] int_arr;
        Py_RETURN_NONE;
    }

    if (PyArray_SetBaseObject(reinterpret_cast<PyArrayObject*>(np_array), capsule) == -1) {
        Py_DECREF(np_array);
        Py_DECREF(capsule);
        Py_RETURN_NONE;
    }
    
    return np_array;
}

static PyObject* convertToNumpy(float** paramList, int rows, int cols) {
    import_array();
    npy_intp dims[2] = {rows, cols};
    PyObject* np_array = PyArray_SimpleNew(2, dims, NPY_FLOAT32);
    if (!np_array) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create NumPy array");
        return NULL;
    }

    float* np_data = (float*)PyArray_DATA((PyArrayObject*)np_array);

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            np_data[i * cols + j] = paramList[i][j];
        }
    }

    return np_array;
}
/*
 * Convert curves as C++ float arrays to Numpy array.
 * Float arrays must be on heap memory and the function will be responsible for freeing memory.
 * 
 * @param params    array to be converted to list
 * @param len       length of the array
 * @param return_n  should return x values of 2D curves or not
 * @return          Numpy array object
 */
static PyObject *toCurve(float *params, int len, bool return_n) {
    /* PASS 2025-02-26 */
    PyObject *value;

    if (return_n) {
        PyObject *xList = genNumpyArange(len);
        PyObject *yList = toNumpyArray(params, len);
        
        PyObject *retr = Py_BuildValue("[O,O]", xList, yList);

        return retr;
    } else return toNumpyArray(params, len);
}
/* Read batch data from iterable python object */
/* 
 * @param data: iterable python object contains batch data
 * @param pySeqs: python str objects
 * @param cppSeqs: c++ str objects (memory managed by python)
 * 
 * @return batch size
 */
static int readBatch(PyObject *data, std::vector<PyObject *> &pySeqs, std::vector<char *> &cppSeqs) {
    /* PASS 2025-02-26 */
    PyObject *iter = PyObject_GetIter(data);
    PyObject *next;
    
    int count = 0;

    while (next = PyIter_Next(iter)) {  // New reference
        if (PyObject_IsInstance(next, SeqRecord)) {
            PyObject *seq = PyObject_GetAttrString(next, "seq");  // New reference
            Py_DECREF(next);
            next = seq;
        }

        char *cppSeq;

        PyObject *pySeq = PyObject_Str(next);
        PyArg_Parse(pySeq, "s", &cppSeq);

        pySeqs.push_back(pySeq);
        cppSeqs.push_back(cppSeq);

        Py_DECREF(next);

        count ++;
    }

    Py_DECREF(iter);

    return count;
}
/* multi-thread shuffle */
static void multiThreadShuffle(
    int nJobs, 
    int count, 
    std::vector<char *> &cppStrs, 
    std::vector<int> &strLens,
    std::random_device &rd,
    int seed
) {
    /* PASS 2025-02-26 */
    std::thread **threads = new std::thread *[nJobs];

    for (int i = 0; i < nJobs; i ++)
        threads[i] = new std::thread(
            [i, count, &cppStrs, &strLens, nJobs, &rd, seed]() {
                for (int j = i; j < count; j += nJobs) {
                    char *cppStr = cppStrs.at(j);
                    char *strEnd = cppStr + strLens.at(j) - 1;
                    std::mt19937 engine(seed < 0 ? rd() : (seed + j));  // Mersenne twister engine
                    std::shuffle(cppStr, strEnd, engine);
                }
            }
        );
        
    for (int i = 0; i < nJobs; i ++) {
        threads[i]->join();
        delete threads[i];
    }

    delete[] threads;
}
#ifdef __cplusplus
extern "C" {
#endif
/* shuffle C/C++ API able to handle many-type Python objects, like str, Seq and SeqRecord */
PyObject *ZCurvePy_shuffle(PyObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-26 */
    static char *kwlist[] = {"records", "ratio", "seed", "n_jobs", NULL};
    int ratio = 1, seed = -1, nJobs = -1;
    PyObject *records;

    // To support more types, seq_or_record should be passed as Python object but not C++ array.
    if (!PyArg_ParseTupleAndKeywords(args, kw, "O|iii", kwlist, &records, &ratio, &seed, &nJobs))
        Py_RETURN_NONE;
    
    if (nJobs <= 0) nJobs = std::thread::hardware_concurrency();

    std::random_device rd;  // Random seed device
    
    std::vector<char *> cppStrs;
    std::vector<int> strLens;

    PyObject *iter = PyObject_GetIter(records);
    PyObject *next;
    int count = 0;

    while (next = PyIter_Next(iter)) {
        // PyObject_GetAttrString will create a new reference so it should be delete correctly.
        if (PyObject_IsInstance(next, SeqRecord)) {
            PyObject *seq = PyObject_GetAttrString(next, "seq");
            Py_DECREF(next);
            next = seq;
        }
    
        // PyObject_Str will create a new reference so it should be delete correctly.
        PyObject *pyStr = PyObject_Str(next);
        int len = (int) PyObject_Length(pyStr);
        const char *origin = PyUnicode_AsUTF8(pyStr);
        
        for (int i = 0; i < ratio; i ++) {
            char *cppStr = new char[len + 1];  
            
            cppStrs.push_back(cppStr);
            strLens.push_back(len);

            strcpy(cppStr, origin);

            count ++;
        }

        Py_DECREF(next);
        Py_DECREF(pyStr);
    }

    Py_DECREF(iter);
    
    if (nJobs > 1)
        multiThreadShuffle(nJobs, count, cppStrs, strLens, rd, seed);
    else for (int j = 0; j < count; j ++) {
        char *cppStr = cppStrs.at(j);
        char *strEnd = cppStr + strLens.at(j) - 1;
        std::mt19937 engine(seed < 0 ? rd() : (seed + j));
        std::shuffle(cppStr, strEnd, engine);
    }

    PyObject *retr = PyList_New(count);

    for (int i = 0; i < count; i ++) {
        PyObject *value = Py_BuildValue("s", cppStrs.at(i));
        PyList_SET_ITEM(retr, i, value);
        delete[] cppStrs.at(i);
    }
    
    return retr;
}
#ifdef __cplusplus
}
#endif
/* convert z-curve coordinate to base symbol */
/* @param vector: z-curve coordinate at a point
 * @return base symbol
 */
static char getBaseSymbol(double *vector) {
    /* PASS 2025-03-02 */
    double dist, distX, distY, distZ;

    // A
    distX = std::abs(vector[X] - 1);
    distY = std::abs(vector[Y] - 1);
    distZ = std::abs(vector[Z] - 1);
    dist = distX + distY + distZ;
    if (dist < 2) return 'A';

    // T
    distX = std::abs(vector[X] + 1);
    distY = std::abs(vector[Y] + 1);
    distZ = std::abs(vector[Z] - 1);
    dist = distX + distY + distZ;
    if (dist < 2) return 'T';

    // G
    distX = std::abs(vector[X] - 1);
    distY = std::abs(vector[Y] + 1);
    distZ = std::abs(vector[Z] + 1);
    dist = distX + distY + distZ;
    if (dist < 2) return 'G';

    // C
    distX = std::abs(vector[X] + 1);
    distY = std::abs(vector[Y] - 1);
    distZ = std::abs(vector[Z] + 1);
    dist = distX + distY + distZ;
    if (dist < 2) return 'C';

    return 'N';
}
/* convert a three-dimentional curve to nucleic sequence */
/*
 * @param params: z-curve parameters of a single sequence
 * @param seqbuf: sequence buffer for decoder
 * @param kValues: assist in parsing profile slope parameters
 * @param length: the length of the origin sequence
 * @param mode:   the mode that plotter coding the sequence
 */
static void decodeCurve(
    double **params, 
    char *seqbuf, 
    double *kValues, 
    int length, 
    int mode
) {
    /* PASS 2025-03-02 */
    int i;
    double vector[3];
    double lastPoint[3] = {0, 0, 0};
    switch(mode) {
        case 0: for (i = 0; i < length; i ++) {
                    vector[X] = params[X][i] - lastPoint[X];
                    vector[Y] = params[Y][i] - lastPoint[Y];
                    vector[Z] = params[Z][i] - lastPoint[Z];
                    seqbuf[i] = getBaseSymbol(vector);
                    lastPoint[X] = params[X][i];
                    lastPoint[Y] = params[Y][i];
                    lastPoint[Z] = params[Z][i];
                }
                seqbuf[i] = 0;
                break;
        case 1: for (i = 0; i < length; i ++) {
                    vector[X] = params[X][i] - lastPoint[X] + kValues[X];
                    vector[Y] = params[Y][i] - lastPoint[Y] + kValues[Y];
                    vector[Z] = params[Z][i] - lastPoint[Z] + kValues[Z];
                    seqbuf[i] = getBaseSymbol(vector);
                    lastPoint[X] = params[X][i];
                    lastPoint[Y] = params[Y][i];
                    lastPoint[Z] = params[Z][i];
                }
                seqbuf[i] = 0;
                break;
        case 2: for (i = 0; i < length; i ++) {
                    vector[X] = params[X][i];
                    vector[Y] = params[Y][i];
                    vector[Z] = params[Z][i];
                    seqbuf[i] = getBaseSymbol(vector);
                }
                seqbuf[i] = 0;
    }
}
/* read curves from Python list */
static void readCurves(PyObject *data, double ***paramList, int *lengths) {
    /* PASS 2025-03-02 */
    int i = 0;
    PyObject *iter = PyObject_GetIter(data);
    PyObject *next;

    while (next = PyIter_Next(iter)) {
        int j;
        paramList[i] = new double* [3];

        PyObject *_iter = PyObject_GetIter(next);
        PyObject *nextValue;

        PyObject *xValues = PyIter_Next(_iter);
        PyObject *yValues = PyIter_Next(_iter);
        PyObject *zValues = PyIter_Next(_iter);

        Py_DECREF(_iter);

        int length = (int) PyObject_Length(xValues);
        lengths[i] = length;

        paramList[i][X] = new double[length];
        paramList[i][Y] = new double[length];
        paramList[i][Z] = new double[length];

        j = 0, _iter = PyObject_GetIter(xValues);
        while(nextValue = PyIter_Next(_iter)) {
            PyArg_Parse(nextValue, "d", &(paramList[i][X][j]));
            Py_DECREF(nextValue);
            j ++;
        }
        Py_DECREF(_iter);
        Py_DECREF(xValues);

        j = 0, _iter = PyObject_GetIter(yValues);
        while(nextValue = PyIter_Next(_iter)) {
            PyArg_Parse(nextValue, "d", &(paramList[i][Y][j]));
            Py_DECREF(nextValue);
            j ++;
        }
        Py_DECREF(_iter);
        Py_DECREF(yValues);

        j = 0, _iter = PyObject_GetIter(zValues);
        while(nextValue = PyIter_Next(_iter)) {
            PyArg_Parse(nextValue, "d", &(paramList[i][Z][j]));
            Py_DECREF(nextValue);
            j ++;
        }
        Py_DECREF(_iter);
        Py_DECREF(zValues);
        
        Py_DECREF(next);
        i ++;
    }

    Py_DECREF(iter);
}
/* decoding z-curves through decoding */
static void multiThreadDecoding(
    double ***paramList, 
    char **cppSeqs, 
    double **kValueList, 
    int *lengths, 
    int size, 
    int nJobs, 
    int mode
) {
    /* PASS 2025-03-02 */
    std::thread **threads = new std::thread *[nJobs];
    
    for (int i = 0; i < nJobs; i ++) {
        threads[i] = new std::thread(
            [i, paramList, cppSeqs, kValueList, lengths, size, mode, nJobs]{
                for (int j = i; j < size; j += nJobs) {
                    cppSeqs[j] = new char[lengths[j] + 1];
                    decodeCurve(paramList[j], cppSeqs[j], kValueList[j], lengths[j], mode);
                }
            }
        );
    }

    for (int i = 0; i < nJobs; i ++) {
        threads[i]->join();
        delete threads[i];
    }

    delete[] threads;
}
#ifdef __cplusplus
extern "C" {
#endif
/* decoding z-curves */
PyObject *ZCurvePy_decode(PyObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-03-02 */
    static char *kwlist[] = {"data", "k_values", "mode", "n_jobs", NULL};
    PyObject *data = NULL;
    PyObject *kValues = NULL;
    char *strMode = NULL;
    int mode = 0, nJobs = 0;

    // To support more types, seq_or_record should be passed as Python object but not C++ array.
    if (!PyArg_ParseTupleAndKeywords(args, kw, "O|Osi", kwlist, &data, &kValues, &strMode, &nJobs))
        Py_RETURN_NONE;
    
    if (nJobs <= 0) nJobs = std::thread::hardware_concurrency();

    if (strMode) for (int i = 0; i < 3; i ++)
        if (!strcmp(strMode, plotterMode[i])) {
            mode = i;
            break;
        }

    int size = (int) PyObject_Length(data);
    int *lengths = new int[size];
    double **kValueList = new double*[size];
    double ***paramList = new double**[size];
    char **cppSeqs = new char *[size];
    readCurves(data, paramList, lengths);

    if (kValues) {
        PyObject *iter = PyObject_GetIter(kValues);
        PyObject *next;
        int k = 0;

        while (next = PyIter_Next(iter)) {
            kValueList[k] = new double[3];
            PyObject *_iter = PyObject_GetIter(next);
            
            PyObject *xKValue = PyIter_Next(_iter);
            PyObject *yKValue = PyIter_Next(_iter);
            PyObject *zKValue = PyIter_Next(_iter);

            PyArg_Parse(xKValue, "d", &(kValueList[k][X]));
            PyArg_Parse(yKValue, "d", &(kValueList[k][Y]));
            PyArg_Parse(zKValue, "d", &(kValueList[k][Z]));
            
            Py_DECREF(xKValue);
            Py_DECREF(yKValue);
            Py_DECREF(zKValue);
            Py_DECREF(_iter);
            Py_DECREF(next);
            k ++;
        }

        Py_DECREF(iter);
    } else if (mode == 1) mode = 0;

    if (nJobs > 1)
        multiThreadDecoding(paramList, cppSeqs, kValueList, lengths, size, nJobs, mode);
    else for (int i = 0; i < size; i ++) {
        cppSeqs[i] = new char[lengths[i] + 1];
        decodeCurve(paramList[i], cppSeqs[i], kValueList[i], lengths[i], mode);
    }

    PyObject *retr = PyList_New(size);

    for (int i = 0; i < size; i ++) {
        PyObject *seq = Py_BuildValue("s", cppSeqs[i]);
        PyList_SET_ITEM(retr, i, seq);
        delete[] cppSeqs[i];
        if (kValues) delete[] kValueList[i];
        for (int j = 0; j < 3; j ++)
            delete[] paramList[i][j];
        delete[] paramList[i];
    }

    delete[] kValueList;
    delete[] cppSeqs;
    delete[] paramList;
    delete[] lengths;

    return retr;
}
#ifdef __cplusplus
}
#endif
/* ZCurveEncoder python object */
typedef struct {
    PyObject_HEAD
    /* 
     * A Python str stores nucleic acid sequence information.
     * It is a completely 'private' member that can only be handled by ZCurveEncoder itself.
     * The C++ object's char array member shares the same memory with pyStr.
     */
    PyObject *pyStr;
    char *cppStr;
    int len;
} ZCurveEncoderObject;
/* ZCurveEncoder.__del__ */
/* Deal with the memory of cppObject and the private Python str */
static void ZCurveEncoder_dealloc(ZCurveEncoderObject *self) {
    /* PASS 2025-02-25 */
    Py_XDECREF(self->pyStr);
    Py_TYPE(self)->tp_free((PyObject *) self);
}
/* ZCurveEncoder.__new__ */
static PyObject *ZCurveEncoder_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    /* PASS 2025-02-25 */
    ZCurveEncoderObject *self;
    
    self = (ZCurveEncoderObject *) type->tp_alloc(type, 0);
    self->pyStr = NULL;

    return (PyObject *) self;
}
/* ZCurveEncoder.__init__ */
/* 
 * The init of ZCurveEncoder
 */
static int ZCurveEncoder_init(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    static char *kwlist[] = {"seq_or_record", NULL};
    PyObject *pySeq;
    bool decRefAttr = false;

    // To support more types, seq_or_record should be passed as Python object but not C++ array.
    if (!PyArg_ParseTupleAndKeywords(args, kw, "O", kwlist, &pySeq))
        return -1;

    // PyObject_GetAttrString will create a new reference so it should be delete correctly.
    if (PyObject_IsInstance(pySeq, SeqRecord)) {
        pySeq = PyObject_GetAttrString(pySeq, "seq");
        decRefAttr = true;
    }

    self->pyStr = PyObject_Str(pySeq);
    // PyArg_Parse don't request heap memory.
    PyArg_Parse(self->pyStr, "s", &(self->cppStr));
    self->len = (int) strlen(self->cppStr);

    if (decRefAttr) Py_DECREF(pySeq);

    return 0;
}
/* ZCurveEncoder.__repr__ */
/*
 * Represent the current sequence information being handled by ZCurveEncoder.
 *
 * When the length of sequence less than 60, it displays the complete sequence;
 * else it only displays the opening part and the ending part.
 * 
 * Call by PyObject_Str and PyObject_Repr
 */
static PyObject *ZCurveEncoder_repr(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    char message[75], *pseq = self->cppStr;
    int l;
    
    if ((l = self->len) <= 60)
        strcat(strcat(strcpy(message, "ZCurveEncoder(\""), pseq), "\")");
    else {
        strncat(strcpy(message, "ZCurveEncoder(\""), pseq, 29);
        strcat(strcat(strcpy(message + 40, "..."), pseq + l - 29), "\")");
    }

    return Py_BuildValue("s", message);
}
/* ZCurveEncoder.genome_order_index */
/*
 * Calculate genome order index: S = a^2 + t^2 + c^2 + g^2
 */
static PyObject *ZCurveEncoder_genomeOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", genomeOrderIndex(self->cppStr, self->len));
}
/*
 * Calculate RY order index: S = (a + g)^2 + (t + c)^2
 */
static PyObject *ZCurveEncoder_ryOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", ryOrderIndex(self->cppStr, self->len));
}
/*
 * Calculate MK order index: S = (a + c)^2 + (t + g)^2
 */
static PyObject *ZCurveEncoder_mkOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", mkOrderIndex(self->cppStr, self->len));
}
/* ZCurveEncoder.WS_order_index */
/*
 * Calculate WS order index: S = (a + t)^2 + (g + c)^2
 */
static PyObject *ZCurveEncoder_wsOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", wsOrderIndex(self->cppStr, self->len));
}
/* ZCurveEncoder.AT_order_index */
/*
 * Calculate AT order index: S = a^2 + t^2
 */
static PyObject *ZCurveEncoder_atOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", atOrderIndex(self->cppStr, self->len));
}
/* ZCurveEncoder.GC_order_index */
/*
 * Calculate GC order index: S = g^2 + c^2
 */
static PyObject *ZCurveEncoder_gcOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", gcOrderIndex(self->cppStr, self->len));
}
/* ZCurveEncoder.CpG_order_index */
/*
 * Calculate GC order index: S = p(CpG)^2 + p(_CpG)^2
 */
static PyObject *ZCurveEncoder_CpGOrderIndex(ZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    return Py_BuildValue("f", CpGOrderIndex(self->cppStr, self->len));
}
/* ZCurveEncoder.mononucl_transform */
/*
 * Do non-phase mononucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_monoTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    float *params = new float[3]();
    bool freq = false;
    bool local = false;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|bb", kwListTrans, &freq, &local))
        Py_RETURN_NONE;

    if (local) freq = true;

    monoTrans(self->cppStr, self->len, params, freq, local);

    return toNumpyArray(params, 3);
}
/* ZCurveEncoder.dinucl_transform */
/*
 * Do non-phase dinucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_diTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    float *params = new float[12]();
    bool freq = false;
    bool local = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|bb", kwListTrans, &freq, &local))
        Py_RETURN_NONE;
    
    if (local) freq = true;
    
    diTrans(self->cppStr, self->len, params, freq, local);

    return toNumpyArray(params, 12);
}
/* ZCurveEncoder.trinucl_transform */
/*
 * Do non-phase trinucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_triTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    float *params = new float[48]();
    bool freq = false;
    bool local = false;
    
    if (!PyArg_ParseTupleAndKeywords(args, kw, "|bb", kwListTrans, &freq, &local))
        Py_RETURN_NONE;

    if (local) freq = true;
    
    triTrans(self->cppStr, self->len, params, freq, local);

    return toNumpyArray(params, 48);
}
/* ZCurveEncoder.mononucl_phase_transform */
/*
 * Do phase-specific mononucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_monoPhaseTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    bool freq = false;
    bool local = false;
    int phase = 3;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListPhaseTrans, &phase, &freq, &local))
        Py_RETURN_NONE;

    float *params = new float[6 * 3]();

    if (phase <= 0) phase = 1;
    if (local) freq = true;
    
    monoPhaseTrans(self->cppStr, self->len, params, phase, freq, local);

    return toNumpyArray(params, 3 * phase);
}
/* ZCurveEncoder.dinucl_phase_transform */
/*
 * Do phase-specific dinucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_diPhaseTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    bool freq = false;
    bool local = false;
    int phase = 3;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListPhaseTrans, &phase, &freq, &local))
        Py_RETURN_NONE;
    
    float *params = new float[6 * 12]();

    if (phase <= 0) phase = 1;
    if (local) freq = true;

    diPhaseTrans(self->cppStr, self->len, params, phase, freq, local);
    
    return toNumpyArray(params, phase * 12);
}
/* ZCurveEncoder.trinucl_phase_transform */
/*
 * Do phase-specific trinucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_triPhaseTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    bool freq = false;
    bool local = false;
    int phase = 3;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListPhaseTrans, &phase, &freq, &local))
        Py_RETURN_NONE;
    
    float *params = new float[6 * 48]();

    if (phase <= 0) phase = 1;
    if (local) freq = true;

    triPhaseTrans(self->cppStr, self->len, params, phase, freq, local);

    return toNumpyArray(params, phase * 48);
}
/* ZCurveEncoder.k_nucl_phase_transform */
/*
 * Do phase-specific k-nucleotide Z-curve transform
 */
static PyObject *ZCurveEncoder_kPhaseTrans(ZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    bool freq = false;
    bool local = false;
    int phase = 3, n = 3;
    int i, k;
    static char *kwlist[] = {"k", "phase", "freq", "local", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|iibb", kwlist, &n, &phase, &freq, &local))
        Py_RETURN_NONE;

    for (i = 0, k = 1; i < n - 1; i ++) k *= 4;
    float *params = new float[phase * k * 3]();
    
    if (phase <= 0) phase = 1;
    if (local) freq = true;

    kPhaseTrans(self->cppStr, self->len, params, n, phase, freq, local);
    return toNumpyArray(params, 3 * phase * k);
}

/* ZCurveEncoder's Member Methods */
static PyMethodDef ZCurveEncoder_methods[] = {
    {"genome_order_index", (PyCFunction) ZCurveEncoder_genomeOrderIndex, METH_NOARGS, NULL},
    {"RY_order_index", (PyCFunction) ZCurveEncoder_ryOrderIndex, METH_NOARGS, NULL},
    {"MK_order_index", (PyCFunction) ZCurveEncoder_mkOrderIndex, METH_NOARGS, NULL},
    {"WS_order_index", (PyCFunction) ZCurveEncoder_wsOrderIndex, METH_NOARGS, NULL},
    {"AT_order_index", (PyCFunction) ZCurveEncoder_atOrderIndex, METH_NOARGS, NULL},
    {"GC_order_index", (PyCFunction) ZCurveEncoder_gcOrderIndex, METH_NOARGS, NULL},
    {"CpG_order_index", (PyCFunction) ZCurveEncoder_CpGOrderIndex, METH_NOARGS, NULL},
    {"mononucl_transform", (PyCFunction) ZCurveEncoder_monoTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"dinucl_transform", (PyCFunction) ZCurveEncoder_diTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"trinucl_transform", (PyCFunction) ZCurveEncoder_triTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"mononucl_phase_transform", (PyCFunction) ZCurveEncoder_monoPhaseTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"dinucl_phase_transform", (PyCFunction) ZCurveEncoder_diPhaseTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"trinucl_phase_transform", (PyCFunction) ZCurveEncoder_triPhaseTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {"k_nucl_phase_transform", (PyCFunction) ZCurveEncoder_kPhaseTrans, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

/* Python Type Object ZCurveEncoder*/
PyTypeObject ZCurveEncoderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_ZCurvePy.ZCurveEncoder",
    sizeof(ZCurveEncoderObject),
    0,
    (destructor) ZCurveEncoder_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    (reprfunc) ZCurveEncoder_repr,
    NULL, /* tp_as_number */
    NULL, /* tp_sq_methods */
    NULL, /* tp_mp_methods */
    NULL, /* tp_hash */
    NULL, /* tp_call */
    NULL, /* tp_str */
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    NULL,
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tprichcmpfunc*/
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */
    NULL, /* tp_iternext */
    ZCurveEncoder_methods,
    NULL, /* tp_members */
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */
    NULL, /* tp_descr_get */
    NULL, /* tp_descr_set */
    NULL, /* tp_dictoffset */
    (initproc) ZCurveEncoder_init,
    NULL, /* tp_alloc */
    ZCurveEncoder_new
};
/* ZCurvePlotter Python Object */
typedef struct ZCurvePlotterObject {
    PyObject_HEAD
    /* 
     * A Python str stores nucleic acid sequence information.
     * It is a completely 'private' member that can only be handled by ZCurvePlotter itself.
     * The C++ object's char array member shares the same memory with pyStr.
     */
    PyObject *pyStr;
    /* The same as ZCurveEncoder Python Object*/
    int len;
    char *cppStr;
} ZCurvePlotterObject;
/* ZCurvePlotter.__del__ */
static void ZCurvePlotter_dealloc(ZCurvePlotterObject *self) {
    /* PASS 2025-02-25 */
    Py_XDECREF(self->pyStr);
    Py_TYPE(self)->tp_free((PyObject *) self);
};
/* ZCurvePlotter.__new__ */
static PyObject *ZCurvePlotter_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    /* PASS 2025-02-25 */
    ZCurvePlotterObject *self;
    
    self = (ZCurvePlotterObject *) type->tp_alloc(type, 0);
    self->pyStr = NULL;
    self->cppStr = NULL;

    return (PyObject *) self;
}
/* ZCurvePlotter.__init__ */
static int ZCurvePlotter_init(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    static char *kwlist[] = {"seq_or_record", NULL};
    PyObject *seq_or_record;
    bool shouldDecRef = false;

    // To support more types, seq_or_record should be passed as Python object but not C++ array.
    if (!PyArg_ParseTupleAndKeywords(args, kw, "O", kwlist, &seq_or_record))
        return -1;
    // PyObject_GetAttrString will create a new reference so it should be delete correctly.
    if (PyObject_IsInstance(seq_or_record, SeqRecord)) {
        seq_or_record = PyObject_GetAttrString(seq_or_record, "seq");
        shouldDecRef = true;
    }
    // PyObject_Str will create a new reference so it should be delete correctly.
    self->pyStr = PyObject_Str(seq_or_record);
    self->len = (int) PyObject_Length(self->pyStr);
    PyArg_Parse(self->pyStr, "s", &(self->cppStr));
    if (shouldDecRef) Py_DECREF(seq_or_record);

    return 0;
}
/* ZCurvePlotter.__repr__ */
/*
 * Represent the current sequence information being handled by ZCurveEncoder.
 *
 * When the length of sequence less than 60, it displays the complete sequence;
 * else it only displays the opening part and the ending part.
 * 
 * Call by PyObject_Str and PyObject_Repr
 */
static PyObject *
ZCurvePlotter_repr(ZCurvePlotterObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-25 */
    char message[75];
    int l;
    
    if ((l = self->len) <= 60)
        strcat(strcat(strcpy(message, "ZCurvePlotter(\""), self->cppStr), "\")");
    else {
        strncat(strcpy(message, "ZCurvePlotter(\""), self->cppStr, 29);
        strcat(strcat(strcpy(message + 40, "..."), self->cppStr + l - 29), "\")");
    }

    return Py_BuildValue("s", message);
}
/* ZCurvePlotter.z_curve */
static PyObject *
ZCurvePlotter_zCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0, i, j;
    float *params[3];
    bool back = true;

    for (i = 0; i < 3; i ++) params[i] = new float[len];

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    zTrans(self->cppStr, len, params, window);

    PyObject *paramList = PyList_New(0);

    // If should return n, a list of arithmetic progression will be created
    if (back) {
        PyObject *vec = genNumpyArange(len);
        PyList_Append(paramList, vec);
        Py_DECREF(vec);
    }

    for (i = 0; i < 3; i ++) {
        PyObject *vec = toNumpyArray(params[i], len);
        PyList_Append(paramList, vec);  // PyList_Append will create a new reference
        Py_DECREF(vec);
    }

    for (i = 0; i < 3; i ++) delete[] params[i];

    return paramList;
}
/* ZCurvePlotter.RY_disparity */
static PyObject *
ZCurvePlotter_RYDisparity(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    ryTrans(self->cppStr, len, params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}
/* ZCurvePlotter.MK_disparity */
static PyObject *
ZCurvePlotter_MKDisparity(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    mkTrans(self->cppStr, len, params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}
/* ZCurvePlotter.WS_disparity */
static PyObject *
ZCurvePlotter_WSDisparity(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    wsTrans(self->cppStr, len, params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}
/* ZCurvePlotter.AT_disparity */
static PyObject *
ZCurvePlotter_ATDisparity(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    atTrans(self->cppStr, len, params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}
/* ZCurvePlotter.GC_disparity */
static PyObject *
ZCurvePlotter_GCDisparity(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    float *params = new float[len];
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    gcTrans(self->cppStr, len, params, window);
    PyObject *retr = toCurve(params, len, back);
    
    return retr;
}
/* ZCurvePlotter.CpG_prime_curve */
static PyObject *
ZCurvePlotter_CpGPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len - 1, window = 0;
    float *params = new float[len], k;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;
    
    k = CpGPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *value = Py_BuildValue("f", k);
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.x_prime_curve */
static PyObject *
ZCurvePlotter_xPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = xPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *curve = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.y_prime_curve */
static PyObject *
ZCurvePlotter_yPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = yPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *value = Py_BuildValue("f", k);
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.z_prime_curve */
static PyObject *
ZCurvePlotter_zPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = zPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *value = Py_BuildValue("f", k);
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.z_prime_curve */
static PyObject *
ZCurvePlotter_atPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = atPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *value = Py_BuildValue("f", k);
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.z_prime_curve */
static PyObject *
ZCurvePlotter_gcPrimeCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, window = 0;
    bool back = true;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ib", kwListCurve, &window, &back))
        Py_RETURN_NONE;

    float *params = new float[len], k;
    k = gcPrimeTrans(self->cppStr, len, params, window);
    PyObject *retr;

    if (back) {
        retr = toCurve(params, len, back);
        PyObject *value = Py_BuildValue("f", k);
        PyList_Append(retr, value);
        Py_DECREF(value);
    } else {
        PyObject *value = Py_BuildValue("f", k);
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,O)", curve, value);
    }

    return retr;
}
/* ZCurvePlotter.genome_dS_curve */
static PyObject *
ZCurvePlotter_genomeDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;
    float *params = new float[len];
    m = genomeDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.RY_dS_curve */
static PyObject *
ZCurvePlotter_ryDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = ryDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.MK_dS_curve */
static PyObject *
ZCurvePlotter_mkDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = mkDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.WS_dS_curve */
static PyObject *
ZCurvePlotter_wsDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = wsDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.AT_dS_curve */
static PyObject *
ZCurvePlotter_atDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = atDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.GC_dS_curve */
static PyObject *
ZCurvePlotter_gcDeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = gcDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter.CpG_dS_curve */
static PyObject *
ZCurvePlotter_CpGdeltaSCurve(ZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-25 */
    int len = self->len, m, window = 0;
    bool back = true;
    bool onlyM = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|ibb", kwListdSCurve, &window, &back, &onlyM))
        Py_RETURN_NONE;

    float max;

    float *params = new float[len];
    m = CpGDeltaSTrans(self->cppStr, len, params, window, max);
    PyObject *retr;

    if (onlyM) return Py_BuildValue("(i,f)", m, max);

    if (back) {
        PyObject *maxPoint = Py_BuildValue("i", m);
        PyObject *maxValue = Py_BuildValue("f", max);
        retr = toCurve(params, len, back);
        PyList_Append(retr, maxPoint);
        PyList_Append(retr, maxValue);
        Py_DECREF(maxPoint);
        Py_DECREF(maxValue);
    } else {
        PyObject *curve = toCurve(params, len, back);
        retr = Py_BuildValue("(O,i,f)", curve, m, max);
    }
    
    return retr;
}
/* ZCurvePlotter methods */
static PyMethodDef ZCurvePlotter_methods[] = {
    {"z_curve", (PyCFunction) ZCurvePlotter_zCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"RY_disparity", (PyCFunction) ZCurvePlotter_RYDisparity, METH_VARARGS|METH_KEYWORDS, NULL},
    {"MK_disparity", (PyCFunction) ZCurvePlotter_MKDisparity, METH_VARARGS|METH_KEYWORDS, NULL},
    {"WS_disparity", (PyCFunction) ZCurvePlotter_WSDisparity, METH_VARARGS|METH_KEYWORDS, NULL},
    {"AT_disparity", (PyCFunction) ZCurvePlotter_ATDisparity, METH_VARARGS|METH_KEYWORDS, NULL},
    {"GC_disparity", (PyCFunction) ZCurvePlotter_GCDisparity, METH_VARARGS|METH_KEYWORDS, NULL},
    {"x_prime_curve", (PyCFunction) ZCurvePlotter_xPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"y_prime_curve", (PyCFunction) ZCurvePlotter_yPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"z_prime_curve", (PyCFunction) ZCurvePlotter_zPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"AT_prime_curve", (PyCFunction) ZCurvePlotter_atPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"GC_prime_curve", (PyCFunction) ZCurvePlotter_gcPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"CpG_prime_curve", (PyCFunction) ZCurvePlotter_CpGPrimeCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"genome_dS_curve", (PyCFunction) ZCurvePlotter_genomeDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"RY_dS_curve", (PyCFunction) ZCurvePlotter_ryDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"MK_dS_curve", (PyCFunction) ZCurvePlotter_mkDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"WS_dS_curve", (PyCFunction) ZCurvePlotter_wsDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"AT_dS_curve", (PyCFunction) ZCurvePlotter_atDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"GC_dS_curve", (PyCFunction) ZCurvePlotter_gcDeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {"CpG_dS_curve", (PyCFunction) ZCurvePlotter_CpGdeltaSCurve, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};
/* ZCurvePlotter type */
PyTypeObject ZCurvePlotterType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_ZCurvePy.ZCurvePlotter",
    sizeof(ZCurvePlotterObject),
    0,
    (destructor) ZCurvePlotter_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    (reprfunc) ZCurvePlotter_repr,
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    NULL, /* tp_call */
    NULL, /* tp_str */
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    NULL,
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */ 
    NULL, /* tp_iternext */ 
    ZCurvePlotter_methods,
    NULL, /* tp_members */ 
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */ 
    NULL, /* tp_descr_get */ 
    NULL, /* tp_descr_set */ 
    NULL, /* tp_dictoffset */ 
    (initproc) ZCurvePlotter_init,
    NULL, /* tp_alloc */
    ZCurvePlotter_new
};
/* BatchZCurveEncoder Python object */
/*
 * The multi-thread version of ZCurveEncoder
 */
typedef struct BatchZCurveEncoderObject {
    PyObject_HEAD
    int nJobs;  // the number of threads used in coding progress
    int nTrans;  // the number of Z-curve coding layers
    int *kList;  // the list of k-mer length in each layer
    int *phaseList;  // the list of phase in each layer
    bool *freqList;  // the list of frequencization usage in each layer
    bool *localList;  // the list of local mode usage in each layer
    int *nParamList;  // the list of number of parameters in each layer
    int finalNParams;  // total parameters generated by BatchZCurveEncoder
} BatchZCurveEncoderObject;
/* Print the summary information of BatchZCurveEncoder */
static PyObject *BatchZCurveEncoder_repr(BatchZCurveEncoderObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-02-26 */
    char message[4096];
    strcpy(message, "ZCurveEncoder:\n");

    for (int i = 0; i < self->nTrans; i ++) {
        char item[512];
        // layer index starts from 0
        sprintf(item, "\tlayer: %d  n=%d  phase=%d  frequency=%s  local=%s  n_params=%d\n", i, 
                self->kList[i], self->phaseList[i], self->freqList[i] ? "True " : "False", 
                self->localList[i] ? "True " : "False", self->nParamList[i]);
        strcat(message, item);
    }

    char item[64];
    sprintf(item, "Total Parameters: %d\n", self->finalNParams);
    strcat(message, item);
    sprintf(item, "Thread Count: %d\n", self->nJobs);
    strcat(message, item);

    return Py_BuildValue("s", message);
}
/* Reset the hyper-parameters */
/* 
 * Util for BatchZCurveEncoder. (Not PyCFunction)
 * @param pyObject: BatchZCurveEncoder Python object
 */
static void resetParams(BatchZCurveEncoderObject *pyObject) {
    /* PASS 2025-02-26 */
    // Reset the list of k-mer length in each layer
    delete[] pyObject->kList;
    pyObject->kList = NULL;
    // Reset the list of phase in each layer
    delete[] pyObject->phaseList;
    pyObject->phaseList = NULL;
    // Reset the frequencization usage in each layer
    delete[] pyObject->freqList;
    pyObject->freqList = NULL;
    // Reset list of local mode usage in each layer
    delete[] pyObject->localList;
    pyObject->localList = NULL;
    // Reset the list of number of parameters in each layer
    delete[] pyObject->nParamList;
    pyObject->nParamList = NULL;
    // Reset number of total parameters generated
    pyObject->finalNParams = 0;
}
/* Reload the hyper-parameters */
/* 
 * Util for BatchZCurveEncoder. (Not PyCFunction)
 * @param pyObject: BatchZCurveEncoder Python object
 * @param hyperParams: Python Iterable object contains Python dicts
 */
static void BatchZCurveEncoder_loadParams(BatchZCurveEncoderObject *pyObject, PyObject *hyperParams) {
    /* PASS 2025-02-26 */
    resetParams(pyObject);
    
    pyObject->nTrans = (int) PyObject_Length(hyperParams);

    // If no hyper-params given, just reset states
    if (pyObject->nTrans <= 0) return;

    pyObject->kList = new int[pyObject->nTrans];
    pyObject->phaseList = new int[pyObject->nTrans];
    pyObject->freqList = new bool[pyObject->nTrans];
    pyObject->localList = new bool[pyObject->nTrans];
    pyObject->nParamList = new int[pyObject->nTrans];

    PyObject *iter = PyObject_GetIter(hyperParams);  // New Reference
    PyObject *next;

    int i = 0, j;

    while (next = PyIter_Next(iter) /* New Reference */) {
        /* PyDict_GetItem borrow reference so do not DecRef */
        // 'n' is a necessary param and must be set in each layer
        PyArg_Parse(PyDict_GetItem(next, keyK), "i", &(pyObject->kList[i]));

        // 'phase' is an optional param
        if (PyDict_Contains(next, keyPhase)) {
            int phase;
            PyArg_Parse(PyDict_GetItem(next, keyPhase), "i", &phase);
            pyObject->phaseList[i] = phase <= 0 ? 1 : phase;
        } else pyObject->phaseList[i] = 3;  // Default value: 3

        // 'frequency' is an optional param 
        if (PyDict_Contains(next, keyFreq)) {
            PyArg_Parse(PyDict_GetItem(next, keyFreq), "b", &(pyObject->freqList[i]));
        } else pyObject->freqList[i] = false;  // Default value: false

        // 'local' is an optional param
        if (PyDict_Contains(next, keyLocal)) {
            PyArg_Parse(PyDict_GetItem(next, keyLocal), "b", &(pyObject->localList[i]));
            /* If local mode is set to true, 'frequency' is forced to be set to true */
            if (pyObject->localList[i]) pyObject->freqList[i] = true;
        } else pyObject->localList[i] = false;  // Default value: false

        Py_DECREF(next);
        i ++;
    }

    Py_DECREF(iter);


    // Calculate number of parameters of each layer and total number of parameters
    for (i = 0; i < pyObject->nTrans; i ++) {
        int nParams = 1;

        for (j = 0; j < pyObject->kList[i] - 1; j ++)
            nParams *= 4;
        
        nParams = nParams * pyObject->phaseList[i] * 3;
        pyObject->nParamList[i] = nParams;
        pyObject->finalNParams += nParams;
    }
}
/* Coding process using multi-thread */
/* 
 * Util for BatchZCurveEncoder. (Not PyCFunction)
 * @param paramList: temporary storage of params
 * @param count: the size if paramList
 * @param cppSeqs: target sequences as C/C++ char array
 * @param pyObject: BatchZCurveEncoder Python object
 */
static void multiThreadCoding(float **paramList, int count,std::vector<char *> &cppSeqs, BatchZCurveEncoderObject *self) {
    /* PASS 2025-02-26 */
    int nJobs = self->nJobs;
    std::thread **threads = new std::thread *[nJobs];
    
    for (int i = 0; i < nJobs; i ++)
        // Thread tasks are assigned according to phase location
        threads[i] = new std::thread(
            [i, paramList, &cppSeqs, count, nJobs, self](){
                for (int j = i; j < count; j += nJobs) {
                    float *head = paramList[j];
                    int length = (int) strlen(cppSeqs.at(j));
                    
                    for (int k = 0; k < self->nTrans; k ++) {
                        kPhaseTrans(cppSeqs.at(j), length, head, 
                                    self->kList[k], self->phaseList[k], 
                                    self->freqList[k], self->localList[k]);
                        head += self->nParamList[k];
                    }
                }
            }
        );
    
    for (int i = 0; i < nJobs; i ++) {
        threads[i]->join();
        delete threads[i];
    }

    delete[] threads;
}
/* BatchZCurveEncoder.__new__ */
static PyObject *BatchZCurveEncoder_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    /* PASS 2025-02-26 */
    BatchZCurveEncoderObject *self;
    
    self = (BatchZCurveEncoderObject *) type->tp_alloc(type, 0);
    // Init hyper-parameters
    self->nTrans = 0;
    self->kList = NULL;
    self->phaseList = NULL;
    self->freqList = NULL;
    self->localList = NULL;
    self->nParamList = NULL;

    return (PyObject *) self;
}
/* BatchZCurveEncoder.__del__ */
static void BatchZCurveEncoder_dealloc(BatchZCurveEncoderObject *self) {
    /* PASS 2025-02-26 */
    resetParams(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
};
/* BatchZCurveEncoder.__call__ */
/* 
 * @param batch: iterable python object
 */
static PyObject *BatchZCurveEncoder_call(BatchZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-26 */
    static char *kwlist[] = {"batch", NULL};
    PyObject *data;
    std::vector<char *> cppSeqs;
    std::vector<PyObject *> pySeqs;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O", kwlist, &data))
        Py_RETURN_NONE;
    
    if (self->nTrans == 0)
        return PyList_New(0);
    
    int count = readBatch(data, pySeqs, cppSeqs);
    int finalNParams = self->finalNParams;
    
    float **paramList = new float *[count];
    
    for (int i = 0; i < count; i ++)
        paramList[i] = new float[finalNParams];

    if (self->nJobs > 1)
        multiThreadCoding(paramList, count, cppSeqs, self);
    else for (int j = 0; j < count; j ++) {
        float *head = paramList[j];
        int length = (int) strlen(cppSeqs.at(j));
            
        for (int k = 0; k < self->nTrans; k ++) {
            kPhaseTrans(cppSeqs.at(j), length, head, 
                        self->kList[k], self->phaseList[k], 
                        self->freqList[k], self->localList[k]);
            head += self->nParamList[k];
        }
    }
    
    PyObject *retr = convertToNumpy(paramList, count, finalNParams);

    for (int i = 0; i < count; i ++) {
        Py_XDECREF(pySeqs.at(i));
        delete[] paramList[i];
    }

    delete[] paramList;

    return retr;
}
/* ZCurvePy.BatchZCurveEncoder.dump */
/* Save params into a file instead of return python list
 * 
 * @param batch: batch of sequences to handle
 * @param save_path: path of the file
 * 
 * @return  whether saved successfully or not
 */
static PyObject *BatchZCurveEncoder_dump(BatchZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-26 */
    static char *kwlist[] = {"batch", "save_path", NULL};
    PyObject *data;
    std::vector<char *> cppSeqs;
    std::vector<PyObject *> pySeqs;
    char *savePath = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "Os", kwlist, &data, &savePath))
        Py_RETURN_NONE;
    
    FILE *file = fopen(savePath, "w");

    if (file == NULL || self->nTrans == 0)
        Py_RETURN_FALSE;
    
    int count = readBatch(data, pySeqs, cppSeqs);
    int finalNParams = self->finalNParams;
    
    float **paramList = new float *[count];

    for (int i = 0; i < count; i ++)
        paramList[i] = new float[finalNParams];
    
    if (self->nJobs > 1)
        multiThreadCoding(paramList, count, cppSeqs, self);
    else for (int j = 0; j < count; j ++) {
        float *head = paramList[j];
        int length = (int) strlen(cppSeqs.at(j));
            
        for (int k = 0; k < self->nTrans; k ++) {
            kPhaseTrans(cppSeqs.at(j), length, head, 
                        self->kList[k], self->phaseList[k], 
                        self->freqList[k], self->localList[k]);
            head += self->nParamList[k];
        }
    }

    for (int i = 0; i < count; i ++) {
        int j;
        fprintf(file, "%d,", i);
        for (j = 0; j < finalNParams - 1; j ++)
            fprintf(file, "%.6f,", paramList[i][j]);
        fprintf(file, "%.6f\n", paramList[i][j]);
        Py_XDECREF(pySeqs.at(i));
        delete[] paramList[i];
    }

    delete[] paramList;
    fclose(file);

    Py_RETURN_TRUE;
}
/* BatchZCurveEncoder.__init__ */
/*
 * init function for BatchZCurveEncoder
 * @param hyper_params: Python Iterable object contains Python dicts.
 * @param n_jobs: number of threads used. 
 *                (Determined by number of CPUs when incorrect value given).
 */
static int BatchZCurveEncoder_init(BatchZCurveEncoderObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-02-26 */
    static char *kwList[] = {"hyper_params", "n_jobs", NULL};
    int nJobs = -1;
    PyObject *hyperParams = NULL;  // Borrow reference in every situation (don not DecRef)

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O|i", kwList, &hyperParams, &nJobs))
        return -1;

    if (nJobs <= 0) nJobs = std::thread::hardware_concurrency();

    self->nJobs = nJobs;

    if (hyperParams != NULL)
        BatchZCurveEncoder_loadParams(self, hyperParams);
    return 0;
}
/* ZCurvePy.BatchZCurveEncoder member methods */
static PyMethodDef BatchZCurveEncoder_methods[] = {
    {"dump", (PyCFunction) BatchZCurveEncoder_dump, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};
/* ZCurvePy.BatchZCurveEncoder type */
PyTypeObject BatchZCurveEncoderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_ZCurvePy.BatchZCurveEncoder",
    sizeof(BatchZCurveEncoderObject),
    0,
    (destructor) BatchZCurveEncoder_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    NULL, /* tp_str*/
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    (ternaryfunc) BatchZCurveEncoder_call,
    (reprfunc) BatchZCurveEncoder_repr,
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    NULL,
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */ 
    NULL, /* tp_iternext */ 
    BatchZCurveEncoder_methods,
    NULL, /* tp_members */ 
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */ 
    NULL, /* tp_descr_get */ 
    NULL, /* tp_descr_set */ 
    NULL, /* tp_dictoffset */ 
    (initproc) BatchZCurveEncoder_init,
    NULL, /* tp_alloc */
    BatchZCurveEncoder_new
};
/* ZCurvePy.BatchZCurvePlotterObject */
typedef struct BatchZCurvePlotterObject {
    PyObject_HEAD
    int mode;  // plotter mode choosed from {"accum", "profile", "tetra"}
    int window;  // window size of mean smoothing operation
    int nJobs;  // number of thread used
} BatchZCurvePlotterObject;
/* ZCurvePy.BatchZCurvePlotterObject.__init__ */
static int BatchZCurvePlotter_init(BatchZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-03-01 */
    static char *kwlist[] = {"mode", "window", "n_jobs", NULL};
    int mode = 0;
    int window = 0;
    int nJobs = -1;
    char *strMode = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|sii", kwlist, &strMode, &window, &nJobs))
        return -1;

    if (nJobs <= 0) nJobs = std::thread::hardware_concurrency();

    if (strMode) for (int i = 0; i < 3; i ++)
        if (!strcmp(strMode, plotterMode[i])) {
            mode = i;
            break;
        }

    self->mode = mode;
    self->window = window;
    self->nJobs = nJobs;

    return 0;
}
/* ZCurvePy.BatchZCurvePlotterObject.__repr__ */
static PyObject *BatchZCurvePlotter_repr(BatchZCurvePlotterObject *self, PyObject *Py_UNUSED(ignored)) {
    /* PASS 2025-03-01 */
    char buf[128];
    sprintf(buf, "BatchZCurvePlotter(mode=\"%s\", window=%d, n_jobs=%d)\n", 
            plotterMode[self->mode], self->window, self->nJobs);
    return Py_BuildValue("s", buf);
}
/* ZCurvePy.BatchZCurvePlotterObject.__dealloc__ */
static void BatchZCurvePlotter_dealloc(BatchZCurvePlotterObject *self) {
    /* PASS 2025-03-01 */
    Py_TYPE(self)->tp_free((PyObject *) self);
}
/* plotting z-curves using multi-thread */
/*
 * @param mode:    code of mode choosed from {"accum", "profile", "tetra"}
 * @param params:  temp storage of z-curve params
 * @param kValue:  temp storage of k-values when using "profile" mode
 * @param cppSeqs: sequences as C++ char array
 * @param seqLens: lengths of sequences
 * @param window:  window of mean smoothing
 * @param count:   size of batch dataset
 * @param n_jobs:  number of threads used
 */
static void multiThreadPlotting(
    int mode,
    float ***params,
    float **kValues,
    std::vector<char *> &cppSeqs,
    std::vector<int> &seqLens,
    int window,
    int count, 
    int nJobs
) {
    /* PASS 2025-03-01 */
    std::thread **threads = new std::thread *[nJobs];

    for (int i = 0; i < nJobs; i ++)
        threads[i] = new std::thread(
            [i, mode, nJobs, window, count, params, kValues, &cppSeqs, &seqLens]() {
                switch(mode) {
                    case 0: for (int j = i; j < count; j += nJobs)
                                 zTrans(cppSeqs.at(j), seqLens.at(j), params[j], window);
                            break;
                    case 1: for (int j = i; j < count; j += nJobs) {
                                kValues[j][X] = xPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][X], window);
                                kValues[j][Y] = yPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][Y], window);
                                kValues[j][Z] = zPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][Z], window);
                            }
                            break;
                    case 2: for (int j = i; j < count; j += nJobs)
                                tetrahedron(cppSeqs.at(j), seqLens.at(j), params[j]);
                }
            }
        );

    for (int i = 0; i < nJobs; i ++) {
        threads[i]->join();
        delete threads[i];
    }

    delete[] threads;
}
/* BatchZCurvePlotter.__call__ */
/* run batch z-curve plotter
 * 
 * @param batch:  batch dataset of sequences
 * @param only_k: only return k-values
 */
static PyObject *BatchZCurvePlotter_call(BatchZCurvePlotterObject *self, PyObject *args, PyObject *kw) {
    /* PASS 2025-03-01 */
    static char *kwlist[] = {"batch", "only_k", NULL};
    std::vector<PyObject *> pySeqs;
    std::vector<char *> cppSeqs;
    std::vector<int> seqLens;
    PyObject *batch = NULL;
    bool onlyK = false;

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O|b", kwlist, &batch, &onlyK))
        Py_RETURN_NONE;
    
    int count = readBatch(batch, pySeqs, cppSeqs);
    float ***params = new float **[count];

    for (int i = 0; i < count; i ++) {
        int len = (int) strlen(cppSeqs.at(i));
        seqLens.push_back(len);
        params[i] = new float *[3];
        for (int j = 0; j < 3; j ++)
            params[i][j] = new float[len];
    }

    float **kValues = NULL;
    int mode = self->mode;
    int window = self->window;

    if (mode == 1) {
        kValues = new float *[count];
        for (int i = 0; i < count; i ++)
            kValues[i] = new float[3];
    }
    
    if (self->nJobs > 1)
        multiThreadPlotting(mode, params, kValues, cppSeqs, seqLens, window, count, self->nJobs);
    else {
        switch(mode) {
            case 0: for (int j = 0; j < count; j ++)
                        zTrans(cppSeqs.at(j), seqLens.at(j), params[j], window);
                    break;
            case 1: for (int j = 0; j < count; j ++) {
                        kValues[j][X] = xPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][X], window);
                        kValues[j][Y] = yPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][Y], window);
                        kValues[j][Z] = zPrimeTrans(cppSeqs.at(j), seqLens.at(j), params[j][Z], window);
                    }
                    break;
            case 2: for (int j = 0; j < count; j ++)
                        tetrahedron(cppSeqs.at(j), seqLens.at(j), params[j]);
        }
    }

    PyObject *retr = PyList_New(count);
    
    for (int i = 0; i < count; i ++) {
        PyObject *array = PyList_New(3);
        int len = seqLens.at(i);
        for (int j = 0; j < 3; j ++) {
            if (mode == 1 && onlyK) {
                PyObject *value = Py_BuildValue("f", kValues[i][j]);
                PyList_SET_ITEM(array, j, value);
            } else {
                PyObject *values = PyList_New(len);
                for (int k = 0; k < len; k ++) {
                    PyObject *value = Py_BuildValue("f", params[i][j][k]);
                    PyList_SET_ITEM(values, k, value);
                }
                PyList_SET_ITEM(array, j, values);
            }
            delete[] params[i][j];
        }
        PyList_SET_ITEM(retr, i, array);
        delete[] params[i];
    }

    delete[] params;

    if (kValues) {
        if (!onlyK) {
            PyObject *kValueRetr = PyList_New(count);
            for (int i = 0; i < count; i ++) {
                PyObject *array = PyList_New(3);
                for (int j = 0; j < 3; j ++) {
                    PyObject *value = Py_BuildValue("f", kValues[i][j]);
                    PyList_SET_ITEM(array, j, value);
                }
                PyList_SET_ITEM(kValueRetr, i, array);
                delete[] kValues[i];
            }
            retr = Py_BuildValue("(O,O)", retr, kValueRetr);
        } else for (int i = 0; i < count; i ++)
            delete[] kValues[i];
        delete[] kValues;
    }

    return retr;
}
/* ZCurvePy.BatchZCurveEncoder type */
PyTypeObject BatchZCurvePlotterType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_ZCurvePy.BatchZCurvePlotter",
    sizeof(BatchZCurveEncoderObject),
    0,
    (destructor) BatchZCurvePlotter_dealloc,
    NULL, /* tp_vectorcall_offset */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_as_async */
    NULL, /* tp_str*/
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    (ternaryfunc) BatchZCurvePlotter_call,
    (reprfunc) BatchZCurvePlotter_repr,
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,
    NULL,
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */ 
    NULL, /* tp_iternext */ 
    NULL, /* tp_methods */
    NULL, /* tp_members */ 
    NULL, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */ 
    NULL, /* tp_descr_get */ 
    NULL, /* tp_descr_set */ 
    NULL, /* tp_dictoffset */ 
    (initproc) BatchZCurvePlotter_init,
    NULL, /* tp_alloc */
    PyType_GenericNew,
};
