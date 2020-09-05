#ifndef TOOL_H
#define TOOL_H

#include "../test.h"

namespace owllib {
	class time_conuter{
	public:
		enum Stat {started, ended, uninitialized};
		time_conuter(void)
		{
			_beg = 0;
			_total = 0;
			_stat = uninitialized;
		}
		time_conuter(const time_conuter& timer)
		{
			_beg = timer._beg;
			_total = timer._total;
			_stat = timer._stat;
		}
		const time_conuter& operator= (const time_conuter& timer)
		{
			if(this != &timer)
 			{
				_beg = timer._beg;
				_total = timer._total;
				_stat = timer._stat;
			}
			return *this;
		}
		virtual ~time_conuter(void){}
		void start(void)
		{
			_beg = clock();
			_stat = started; 
		}
		void end(void)
		{ 
			if(_stat == started)
			{	
				_total += clock() - _beg;
				_stat = ended;
			}
		}
		const clock_t total() const
		{
			return _stat == ended ? _total : -1;
		}
		void clear(void){ _total = 0 ;_stat = uninitialized;}
	private:
		Stat _stat;	
		clock_t _total;
		clock_t _beg;
	};	

	template<typename colltype>
		void print_container(const colltype& coll,
		                     const std::string& str = "")
	{
		std::cout << str;
		typename colltype::const_iterator it;
		for(it = coll.begin(); it != coll.end(); ++it)
			std::cout << *it << "\t" ;
		std::cout << std::endl;
	}

	template<typename colltype>
		void file_to_container(colltype& coll,
		                       std::ifstream& fin)
	{
		std::
		istream_iterator<typename colltype::value_type> beg(fin),
			                                            end;
		std::copy(beg, end, std::inserter(coll, coll.end()));
	}
	
	template<typename colltype>
		void container_to_file(colltype& coll,
		                       std::ofstream& fout)
	{
		std::
		ostream_iterator<typename colltype::value_type> beg(fout,"\t");
		std::copy(coll.begin(), coll.end(), beg);
	}

	
	template<typename colltype>
		void look_container(const colltype& date)
	{
		std::cout << "container's type is : "
			<< typeid(colltype).name()
			<< "\n"
			<< "container's value type is : "
			<< typeid(typename colltype::value_type).name()
			<< "\n"
			<< "container's size is:"
			<< date.size()
			<< std::endl;
	}
   
};

#endif 
