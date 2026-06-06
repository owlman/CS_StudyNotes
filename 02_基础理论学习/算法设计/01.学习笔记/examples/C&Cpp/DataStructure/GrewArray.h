#ifndef GREWARRAY_H
#define GREWARRAY_H
#include "structure.h"

namespace owllib
{
	 template<typename type,
			  typename Allocator = std::allocator<type> >
	 class GrewArray{
	 public:	
		typedef type           value_type;
		typedef size_t         size_type;
		typedef ptrdiff_t      diffecence_type;
		typedef type*          pointer;
		typedef const type*    const_pointer;
		typedef type&          reference;
		typedef const type&    const_reference;
	 public:
		 GrewArray(size_type sz = 1,
			       Allocator a = Allocator())
		:_count(0), _size(sz), _alloc(a), _ia(NULL)
		 {
			get_memory();
			std::uninitialized_fill_n(_ia, _size, 0);
		 }
		 GrewArray(const_pointer cap,
			       const size_type sz,
			       Allocator a = Allocator())
		   :_count(sz), _size(sz), _alloc(a), _ia(NULL)
		 {
			 get_memory();
			 std::uninitialized_copy(cap, &cap[sz-1], _ia);
		 }

		 GrewArray(const GrewArray<type>& coll)
			 : _count(coll._count),_size(coll._size), _alloc(coll._alloc), _ia(NULL)
		 {													  
			 get_memory();
			 std::uninitialized_copy(coll.begin(), coll.end(),_ia);
		 }
		 		 
        GrewArray<type>& operator= (const GrewArray<type>& coll)
		{
			if(this == &coll)
				return *this;
			if(_ia != NULL)
			{
				for(size_type i = 0; i < _size; ++i)
					_alloc.destroy(&_ia[i]);
				_alloc.deallocate(_ia, _size);
			}
			_count = coll.count();
			_size = coll.size();
			get_memory();
			std::uninitialized_copy(coll.begin(), coll.end(),_ia);
			return coll;
		}

		 reference operator[] (const size_type index)
		{
			return _ia[index];
		}
		const_reference operator[] (const size_type index) const
		{
			return _ia[index];
		}

		const_pointer begin(void) const
		{
			return _ia;
		}

		const_pointer end(void) const
		{
			return &_ia[_size-1];
		}
		
		const value_type min(void) const
		{
			return *std::min_element(_ia, &_ia[_count]);
		}

        const value_type max(void) const 
		{
			return *std::max_element(_ia, &_ia[_count]);
		}

		const size_type size(void) const
		{ 
			return _size;	
		}
		const size_type count(void) const
		{ 
			return _count;	
		}
		void push(const value_type value)
		{
			//something...
			if(_count > _size-1)
			{
				pointer temp = _ia;
				_size = _size * 2 ;
				get_memory();
				std::uninitialized_copy(temp, &temp[_count-1], _ia);
				for(size_type i = 0; i < _size; ++i)
					_alloc.destroy(&temp[i]);
				_alloc.deallocate(temp, _size/2);
				
			}			
			_ia[_count++] = value;
		}
		const value_type pop(void) 
		{
			//something...;
			return _ia[_count--];
		}

		 ~GrewArray(void)
		{
			for(size_type i = 0; i < _size; ++i)
			{
				_alloc.destroy(&_ia[i]);
			}
			_alloc.deallocate(_ia, _size);
		}
	 private:
 		void get_memory(void)
		{
			_ia = _alloc.allocate(_size);
		}
		size_type _count;
    	size_type _size;
		Allocator _alloc;
		pointer   _ia;
	 };
}
#endif
