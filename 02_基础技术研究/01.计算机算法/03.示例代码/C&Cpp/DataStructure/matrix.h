//
//  matrix.h
//
//  Created by lingjie on 2008-5-4.
//
//

#ifndef MATRIX_H
#define MATRIX_H
#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <vector>
namespace owllib {
	template<typename Ty>
	class matrix {	
	private:;
		//proxy class vec:
        template<typename type>
        class vec{
        public:
			vec(size_t sz = 0,
				const type& value = type()) 
				: vect(sz,value){}
			vec(const vec<type>& v): vect(v.vect) {}
			void init(size_t sz = 0,
				      const type value = type())
			{
				std::vector<type>(sz,value).swap(vect);
			}
			void init(const vec<type>& v)
			{
				std::vector<type>(v.vect).swap(vect);
			}
			size_t size(void) const
			{
				return vect.size();
			}
			vec<type>& operator= (const vec<type>& v)
			{
				if(this != &v)
					vect.swap(std::vector<type>(v.vect));
				return *this;
			}
            type& operator[](size_t index)
            {
                try {
					return vect.at(index);
                }
                catch(std::out_of_range& e)
                {
                    std::cout << e.what() << std::endl;
                    throw e;
                }    
            } 
            const type& operator[](size_t index) const 
            {
                try {
					return vect.at(index);
				}
                catch(std::out_of_range& e)
                {
                    std::cout << e.what() << std::endl;
                    throw e;
                }                  
            }                         
        private: 
			std::vector<type> vect;
        }; 
    public:   		
		//constructors
		matrix(size_t lsz = 0,
               size_t rsz = 0,
               const Ty& value = Ty())
		: mat(lsz) 
		{
			for(size_t i = 0; i < mat.size(); ++i)
				mat[i].init(rsz,value);
		}		
		matrix(const matrix<Ty>& cmat)
		:mat(cmat.mat)
		{
			for(size_t i = 0; i < mat.size(); ++i)
			 	mat[i].init(cmat[i]);
		}
        
		//destructors
		~matrix(void)
		{}
		
		//public member methods
		const size_t line_size(void) const
		{
			return mat.size();
		}
		const size_t row_size(void) const
		{
			return mat[0].size();
		}
		const size_t size(void) const
		{
			return size_t(mat.size() * mat[0].size());
		}
        
		//operator member
		matrix<Ty>& operator= (const matrix<Ty>& cmat)
		{
			if(this == &cmat)
				return *this;
			std::vector< vec<Ty> >(cmat.mat).swap(mat);
			for(size_t i =  0; i < mat.size(); ++i)
				mat[i].init(cmat[i]);
			return *this;
		}
		vec<Ty>& operator[] (size_t index)
		{
		    try {
              return mat.at(index);
            }
            catch(std::out_of_range& e)
            {
               std::cout << e.what() << std::endl;
               throw e;
            }
		}
		const vec<Ty>& operator[] (size_t index) const
		{
			try {
               return mat.at(index);
            }
            catch(std::out_of_range& e)
            {
               std::cout << e.what() << std::endl;
               throw e;
            }	
		}
			
	private:
		//date member
		std::vector< vec<Ty> > mat;
	};

	template<typename datatype,typename type>
	matrix<datatype> operator* (const datatype data,
		                        const matrix<type>& mat)
	{
		matrix<datatype> ret(mat.line_size(),mat.row_size());
		for(size_t i = 0;i < mat.line_size(); ++i)
			for(size_t j = 0;j < mat.row_size(); ++j)
				ret[i][j] = mat[i][j] * data;
 
		return matrix<datatype>(ret);
	}
	template<typename datatype,typename type>
	matrix<datatype> operator* (const matrix<type>& mat,
	                            const datatype data)
	{
		return matrix<datatype>(data * mat);
	}
	template<typename type>
	matrix<type> operator+ (const matrix<type>& lmat,
	                        const matrix<type>& rmat)
	{
		try{
			if((lmat.line_size() != rmat.line_size())
				||(lmat.row_size() != rmat.row_size()))
				throw std::string("lmat.line_size() != rmat.line_size() or lmat.row_size() != rmat.row_size()");
		}
		catch(std::string& e)
		{
			std::cout << e << std::endl;
			std::exit(EXIT_FAILURE);
		}
		matrix<type> ret(lmat.line_size(),lmat.row_size());
		for(size_t i = 0;i < lmat.line_size(); ++i)
			for(size_t j = 0;j < lmat.row_size(); ++j)
				ret[i][j] = lmat[i][j] + rmat[i][j];
 
		return matrix<type>(ret);
	}
	template<typename type>
	matrix<type> operator* (const matrix<type>& lmat,
	                        const matrix<type>& rmat)
	{
		try{
			if(lmat.row_size() != rmat.line_size())
				throw std::string("lmat.row_size() != rmat.line_size()!");
		}
		catch(std::string& e)
		{
			std::cout << e << std::endl;
			std ::exit(EXIT_FAILURE);
		}
		matrix<type> ret(lmat.line_size(),rmat.row_size());
		for(size_t i = 0;i < ret.line_size(); ++i)
			for(size_t j = 0;j < ret.row_size(); ++j)
				for(size_t k = 0;k < lmat.row_size(); ++k)
   					ret[i][j] += lmat[i][k] * rmat[k][j];
 
		return matrix<type>(ret);
	}
	template<typename type>
	matrix<type> transpose(const matrix<type>& mat)
	{
		matrix<type> ret(mat.row_size(),mat.line_size());
		for(size_t i = 0;i < mat.line_size(); ++i)
			for(size_t j = 0;j < mat.row_size(); ++j)
				ret[j][i] = mat[i][j];
		return matrix<type>(ret);
	}
	template<typename type>
	std::istream& operator>> (std::istream& in,matrix<type>& mat)
	{
		for(size_t i = 0;i < mat.line_size();++i)
			for(size_t j = 0; j < mat.row_size(); ++j)
				in >> mat[i][j]  ;
		return in;
	}
	template<typename type>
	std::ostream& operator<< (std::ostream& out,matrix<type>& mat)
	{
		 for(size_t i = 0;i < mat.line_size();++i)
		 {
			 for(size_t j = 0; j < mat.row_size(); ++j)
				 out << mat[i][j] << " " ;
			 out << std::endl;
		 }
		 return out;
	}
}
#endif
