#ifndef TEST_OWLLIB_H
#define TEST_OWLLIB_H
#include "structure/structure.h"
#include "algorithm/algorithm.h"

class testOwllib
{
    private:
		class a_task
		{
		public:
			void operator()() const
			{
				std::cout << "this is a function object...\n";
			}
		};		
	public:
		static void testC11_thread()
		{
			// say hello
			std::thread my_thread([]{
				std::cout << "hello, concurrent world!" << std::endl;
			});
			my_thread.join();
			std::thread task_thread{ a_task() };
			task_thread.join();
		}

		static void testMatrix()
		{
			owllib::matrix<int> m(2,3,110), t;

			std::cout << m << std::endl;
			m = transpose(m) + transpose(2*m) + transpose(3*m);
			std::cout << m << std::endl;
			t = m * transpose(m);
			std::cout << t << std::endl;
			t = m;
			std::cout << t << std::endl;
		}

		static void testThreadsafe_LookupTable(bool doremove)
		{
			owllib::Threadsafe_LookupTable<int, std::string> L_table;
			std::vector<std::string> some_name = { "owlman", "batman", "superman" };
			for (unsigned i = 0; i < some_name.size(); ++i)
				L_table.add_or_update_mapping(i, some_name[i]);
			std::map<int, std::string> testmap = L_table.get_map();
			for (std::map<int, std::string>::iterator it = testmap.begin();
			it != testmap.end();
				++it)
			{
				std::cout << it->first << ": " << it->second << std::endl;
			}
			if(doremove)
				L_table.remove_mapping(1);
			if (L_table.value_for(1) != std::string())
				std::cout << "this is " << L_table.value_for(1) << std::endl;
			else
				std::cout << "no value" << std::endl;
		}

		static void testThreadsafe_Queue()
		{
			int tmp = 0;
			owllib::Threadsafe_Queue<int> que;
			
			std::cout << "push 1000 value to the queue..." << std::endl;
			for (int i = 0; i < 1000; ++i) { que.push(i); }
			std::cout << "que.get_size(): " << que.get_size() << std::endl;
			
			std::cout << "pop some value..." << std::endl;
			for (int i = 0; i < 3; ++i)
			{
				std::cout << *que.try_pop() << std::endl;
				std::cout << *que.wait_and_pop() << std::endl;
				que.try_pop(tmp);
				std::cout << tmp << std::endl;
				que.wait_and_pop(tmp);
				std::cout << tmp << std::endl;
			}
			std::cout << "que.get_size(): " << que.get_size() << std::endl;
			
			std::cout << "pop all value..." << std::endl;
			while (!que.empty())
				que.try_pop();

			std::cout << "que.get_size(): " << que.get_size() << std::endl;			
		}

		static void testThreadsafe_List()
		{
			owllib::Threadsafe_list<int> ilist;
			for (int i = 0; i < 10; ++i)
			{
				ilist.push_front(i);
			}
			std::cout << "ilist.get_size(): " << ilist.get_size() << std::endl;
			ilist.for_each([](const int value) {std::printf("%d\n", value); });

			ilist.remove_if([](const int value) {return value == 4; });
			if (!ilist.find_first_if([](const int value) {return value == 4; }))
				std::cout << "4 is remove!" << std::endl;
			std::cout << "ilist.get_size(): " << ilist.get_size() << std::endl;
			ilist.for_each([](const int value) {std::printf("%d\n", value); });

			int total = 0;
			ilist.for_each([&total](const int value) {total += value; });
			std::cout << "ilist.sun = : " << total << std::endl;
		}
};
#endif
