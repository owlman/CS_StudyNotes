#ifndef LIST_H
#define LIST_H

#include "structure.h"

namespace owllib {
	template<typename type>
	class list_item {
	public:
		typedef type value_type;

		list_item(type, list_item<type>*);   
		list_item(const list_item<type>&);      
		const type date () const;                
		const list_item<type>* next() const;     
		void get_date (const type);              
		void get_next (const list_item<type>*);  

		const list_item<type>&
			operator= (const list_item<type>&);  
	
	private:
		type  _date;
		list_item<type>* _next;
	};
	
	template<typename type>
		list_item<type>::list_item(type ia, list_item<type>* p)
	{
		get_date(ia);
		if(p == NULL)
			get_next(NULL);
		else 
		{
			get_next(p->next());
			p->get_next(this);
		}
	}
	
	template<typename type> list_item<type>::
		list_item(const list_item<type>& node)
	{
		get_date(node.date());
		if(node.next() == NULL)
			get_next(NULL);
		else
		{
			get_next(node.next());
			node.get_next(this);
		}
	}

	template<typename type>
		const list_item<type>& list_item<type>::
		operator= (const list_item<type>& node)
	{
		if(this != &node)
		{
			get_date(node.date());
			if(node.next() == NULL)
				get_next(NULL);
			else
			{
				get_next(node.next());
				node.get_next(this);
			}
		}
		return *this;
	}
	
	template<typename type>
		const type 
		list_item<type>::date() const 
	{
		return _date;
	}
	template<typename type> const 
		list_item<type>* list_item<type>::
		next(void) const  
	{
		return _next;
	}
	template<typename type>
		void list_item<type>::
		get_date(const type de)
	{
		_date = de; 
    }	
	template<typename type>
		void list_item<type>::
		get_next( const list_item<type> *pev )
    { 
       _next = ( list_item<type>* )pev;   
    }

	template<typename type> 
	class list{
	public:
		typedef type           value_type;
		typedef size_t         size_type;
		typedef ptrdiff_t      diffecence_type;
		typedef type*          pointer;
		typedef const type*    const_pointer;
		typedef type&          reference;
		typedef const type&    const_reference;
	public:
		list();                              
		list( const list<type>& );       
		~list();                          
		const int size() const;
		bool empty() const;            
		void insert( const type, const type);
		void insert_front( const type );  
		void insert_end( const type );    
		void remove( const type );        
		void remove_all();                  
		void remove_front();                
		const list_item<type>* 
			find(const type);           
		const list<type>&
			operator= (const list<type>&); 
	
	private:
		void down_size();
		void add_size();
		list_item<type> *at_front;
		list_item<type> *at_end;
		list_item<type> *at_move;
		int                _size;
	};

	template<typename type>
		void list<type>::add_size() 
    {
       ++_size; 
    }

	template<typename type>
		void list<type>::down_size() 
    {
       --_size; 
    }

	template<typename type>
		list<type>::list(void)
    { 
       at_front = NULL;
       at_end = NULL;
       _size = 0;
    }

	template<typename type>
		list<type>::~list(void) 
    {
       remove_all();
    }

	template<typename type>
		bool list<type>::
		empty(void) const 
    {
       return size() == 0 ? true : false;
    }

	template<typename type>
		const int list<type>::
		size(void) const
    { 
       return _size;
    }

	template<typename type>
		void list<type>::insert_front(const type iva)
    {
       list_item<type> *pv = 
              new list_item<type>(iva, 0);
       if(!at_front)
       {
           at_front = at_end = pv;
       }
       else 
       {
           pv->get_next(at_front);
           at_front = pv;
       }
       add_size();
    }

	template<typename type>
		void list<type>::insert_end(const type iva) 
	{
       if( at_end == NULL) 
       {
           at_end = at_front = new list_item<type>( iva, 0 );
       }
       else 
           at_end = new list_item<type>( iva, at_end ); 
       add_size();
    }

	template<typename type> void list<type>::
		insert( const type ixa, const type iva ) 
    {
       list_item<type> *pev = 
              ( list_item<type>* )find( iva );
       if( pev == NULL )
       {
		   std::cerr << "err!" ;
           return;
       }
      if( pev == at_front ) 
           insert_front( ixa );
       else
	   {
           new list_item<type>( ixa, pev );
           add_size();
       }
    }

	template<typename type> const 
		list_item<type>* list<type>::
		find( const type iva )
    {
       list_item<type> *at_move = at_front;
       while( at_move != NULL ) 
       {
           if( at_move->date() == iva )
              return at_move;
           at_move = ( list_item<type>* )at_move->next();
           
       }
           return NULL;
    }

	template<typename type>
		void list<type>::remove_front()
    {
       if( at_front )
       {
           list_item <type> *pev = at_front;
           at_front = ( list_item<type>* )at_front->next();
           delete pev;
           down_size();
       }
    }

	template<typename type>
		void list<type>::remove( type iva )
    {
       list_item<type> *pev = at_front;
       while(pev && (pev->date()==iva))
       {
           pev = ( list_item<type>* )pev->next();
           remove_front();
       }
       if( !pev )
           return ;
       list_item<type> *prv = pev;
       pev = ( list_item<type>* )pev->next();
       while( pev ) 
       {
           if( pev->date() == iva ) 
           {
              prv->get_next( pev->next() );          
              down_size();
              delete pev;
              pev = ( list_item<type>* )prv->next();
              if( pev != NULL )
              {
                  at_end = prv;
                  return;
              }
           }
           else 
           {
              prv = pev;
              pev = ( list_item<type>* )pev->next();
           }
       }
    }

	template<typename type>
		void list<type>::remove_all()
    {
       while( at_front )
           remove_front();
       _size = 0;
       at_front = at_end = NULL;
    }
	
}; 
#endif
