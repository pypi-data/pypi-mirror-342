import numpy

H =  numpy.array([[0,0], [0,0]])
f = numpy.zeros((2,1))
F = numpy.array([[9.6652, 5.2115], [7.0732, -7.0879]])
A = numpy.array([[1.0, 0], [-1, 0], [0, 1], [0, -1]])
b = 2*numpy.ones((4,1));
B = numpy.zeros((4,2));

thmin = -1.5*numpy.ones(2)
thmax = 1.5*numpy.ones(2)

from pdaqp import MPQP
mpQP = MPQP(H,f,F,A,b,B,thmin,thmax,out_inds=[0])
mpQP.solve()
#mpQP.plot_regions()
#mpQP.plot_solution()
#mpQP.codegen(dir="codegen", fname="pdaqp")
for cr in mpQP.CRs:
    print(cr.AS)
    print(cr.z)
