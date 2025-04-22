// lzf.i
%module lzf

%{
#include "lzf.h"
%}

// Tell SWIG how to wrap uint64_t
// %include <stdint.i>
// %include <std_vector.i>
// namespace std {
//     %template(VMAVector) vector<VMA>;
// }

%include "lzf.h"