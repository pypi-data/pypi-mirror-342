
#ifndef BALLWALK_HPP
#define BALLWALK_HPP

#include "RandomWalk.hpp"

class BallWalk: public RandomWalk{
    

    public:

        /**
         * @brief initialization of Ball Walk class
         * @param r spread parameter
         * @param thin thin constant
         */
        BallWalk(double r, int thin = 1) : R(r), RandomWalk(thin) {
            
        }

        /**
         * @brief generate values from Ball Walk
         * @param num_steps number of steps wanted to take
         * @param x initial starting point
         * @param A polytope matrixd (Ax <= b)
         * @param b polytope vector (Ax <= b)
         * @param burn number of initial steps to cut
         * @return num_steps by d (dimension of x) matrix
         */
        MatrixXd generateCompleteWalk(const int num_steps, VectorXd& x, const MatrixXd& A, const VectorXd& b, int burn) override;
        
        /**
         * @brief print general type 
         */
        void printType() override;
    
    protected:
        /**
         * @brief spread parameter
         */
        const double R;


};

#endif