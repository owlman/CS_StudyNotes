#ifndef TSQUEUE_H
#define TSQUEUE_H
#include "structure.h"

namespace owllib
{
    template<typename type>
    class Threadsafe_Queue
    {
    private:
        struct node
        {
            std::shared_ptr<type> data;
            std::unique_ptr<node> next;
        };
		std::mutex head_mutex;
		std::mutex tail_mutex;
		std::unique_ptr<node> head;
		node* tail;
		std::condition_variable data_cond;

		node* get_tail() {
			std::lock_guard<std::mutex> tail_lock(tail_mutex);
			return tail;
		}

		std::unique_ptr<node> pop_head() {
			std::unique_ptr<node> old_head = std::move(head);
			head = std::move(old_head->next);
			return old_head;
		}

		std::unique_lock<std::mutex> wait_for_data() {
			std::unique_lock<std::mutex> head_lock(head_mutex);
			data_cond.wait(head_lock,
				[&]{return head.get() != get_tail(); });
			
			return std::move(head_lock);
		}

		std::unique_ptr<node> wait_pop_head() {
			std::unique_lock<std::mutex> head_lock(wait_for_data());
			return pop_head();
		}

		std::unique_ptr<node> wait_pop_head(type& value) {
			std::unique_lock<std::mutex> head_lock(wait_for_data());
			value = std::move(*head->data);
			return pop_head();
		}

		std::unique_ptr<node> try_pop_head() {
			std::lock_guard<std::mutex> head_lock(head_mutex);
			if (head.get() == get_tail())
				return std::unique_ptr<node>();

			return pop_head();
		}

		std::unique_ptr<node> try_pop_head(type& value) {
			std::lock_guard<std::mutex> head_lock(head_mutex);
			if (head.get() == get_tail())
				return std::unique_ptr<node>();

			value = std::move(*head->data);
			return pop_head();
		}
    public:
		Threadsafe_Queue() : head(new node), tail(head.get()){}
		Threadsafe_Queue(const Threadsafe_Queue& other) = delete;
		Threadsafe_Queue& operator=(const Threadsafe_Queue& other) = delete;
        
		std::shared_ptr<type> try_pop() {
			std::unique_ptr<node> old_head = try_pop_head();
			return old_head != std::unique_ptr<node>()?
				      old_head->data : std::shared_ptr<type>();
		}

		bool try_pop(type& value) {
			const std::unique_ptr<node> old_head = try_pop_head(value);
			return old_head != std::unique_ptr<node>();
		}

		std::shared_ptr<type> wait_and_pop() {
			const std::unique_ptr<node> old_head = wait_pop_head();
			return old_head->data;
		}

		void wait_and_pop(type& value) {
			const std::unique_ptr<node> old_head = wait_pop_head(value);
		}

		void push(type new_value) {
			std::shared_ptr<type> new_data(std::make_shared<type>(std::move(new_value)));
			std::unique_ptr<node> ptr(new node);
			{
				std::lock_guard<std::mutex> tail_lock(tail_mutex);
				tail->data = new_data;
				node* const new_tail = ptr.get();
				tail->next = std::move(ptr);
				tail = new_tail;
			}
			data_cond.notify_one();
		}

		bool empty() {
			std::lock_guard<std::mutex> head_lock(head_mutex);
			return (head.get() == get_tail());
		}
		unsigned get_size() {
			unsigned i = 0;
			std::lock_guard<std::mutex> head_lock(head_mutex);
			node* p = head.get();
			while (p != get_tail())
			{
				p = (p->next).get();
				++i;
			}
			return i;
		}
    };
}
#endif