#ifndef TSLIST_H
#define TSLIST_H
#include "structure.h"

namespace owllib
{
    template<typename type>
    class Threadsafe_list
    {
    private:
        struct node
        {
            std::mutex m;
            std::shared_ptr<type> data;
            std::unique_ptr<node> next;

            node(): 
                next() 
            {}

            node(const type& value): 
                data(std::make_shared<type>(value))
            {}            
        };

        node head;
    public:
        Threadsafe_list() 
        {}

        ~Threadsafe_list()
        {
            remove_if([](const node&){return true;});
        }

        Threadsafe_list(const Threadsafe_list& other) =delete;
        Threadsafe_list& operator=(const Threadsafe_list& other) =delete;
        
        void push_front(const type& value)
        {
            std::unique_ptr<node> new_node(new node(value));
            std::lock_guard<std::mutex> ilock(head.m);
            new_node->next = std::move(head.next);
            head.next = std::move(new_node);
        }
        
        template<typename function>
        void for_each(function f)
        {
            node* current = &head;
            std::unique_lock<std::mutex> ilock(head.m);
            while(node* const next = current->next.get())
            {
                std::unique_lock<std::mutex> next_ilock(next->m);
                ilock.unlock();
                f(*next->data);
				current = next;
                ilock = std::move(next_ilock);
            }
        }

        template<typename predicate>
        std::shared_ptr<type> find_first_if(predicate p)
        {
            node* current = &head;
            std::unique_lock<std::mutex> ilock(head.m);
            while(node* const next = current->next.get())
            {
                std::unique_lock<std::mutex> next_ilock(next->m);
                ilock.unlock();
                if(p(*next->data))
                {
                    return next->data;
                }
                current = next;
                ilock = std::move(next_ilock);
            }
            return std::shared_ptr<type>();
        }

		template <typename predicate>
		void remove_if(predicate p)
		{
			node* current = &head;
			std::unique_lock<std::mutex> ilock(head.m);
			while (node* const next = current->next.get())
			{
				std::unique_lock<std::mutex> next_ilock(next->m);
				if (p(*next->data))
				{
					std::unique_ptr<node> old_next = std::move(current->next);
					current->next = std::move(next->next);
					next_ilock.unlock();
				}
				else
				{
					ilock.unlock();
					current = next;
					ilock = std::move(next_ilock);
				}			
			}
		}

		unsigned get_size() {
			unsigned i = 0;
			node* current = &head;
			std::unique_lock<std::mutex> ilock(head.m);
			while (node* const next = current->next.get())
			{
				std::unique_lock<std::mutex> next_ilock(next->m);
				ilock.unlock();
				current = next;
				i++;
				ilock = std::move(next_ilock);
			}
			return i;
		}
    };
}

#endif 