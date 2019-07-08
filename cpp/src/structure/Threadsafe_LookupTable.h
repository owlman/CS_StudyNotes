#ifndef TSLOOKUPTABLE_H
#define TSLOOKUPTABLE_H
#include "structure.h"

namespace owllib
{
    template<typename key, typename value,
             typename hash = std::hash<key> >
    class Threadsafe_LookupTable {
    private:
        class bucketTyoe {
		public:
			typedef std::pair<key, value> bucketValue;
			typedef std::list<bucketValue> bucketData;
			typedef typename bucketData::iterator bucketIterator;
        private:
            bucketData data;
            mutable boost::shared_mutex mutex;

            bucketIterator find_entry_for(const key& ky) {
				return std::find_if(data.begin(), data.end(),
                                    [&](const bucketValue& item)
                                    {return item.first == ky;});
			}
        public:
			boost::shared_mutex& get_mutex() const 	{
				return mutex;
			}
			bucketData& get_data() {
				return data;
			}
            value value_for(const key& ky, const value& defaultVal) {
                boost::shared_lock<boost::shared_mutex> lock(mutex);
                const bucketIterator foundEntry = find_entry_for(ky);
                return (foundEntry == data.end())?
                       defaultVal : foundEntry->second;
            }

            void add_or_update_mapping(const key& ky, const value& val) {
                std::unique_lock<boost::shared_mutex> lock(mutex);
                const bucketIterator foundEntry = find_entry_for(ky);
                if (foundEntry == data.end())
                {
                    data.push_back(bucketValue(ky, val));
                }
                else
                {
                    foundEntry->second = val;
                }
            }

            void remove_mapping(const key& ky) {
                std::unique_lock<boost::shared_mutex> lock(mutex);
                const bucketIterator foundEntry = find_entry_for(ky);
                if (foundEntry != data.end())
                {
                    data.erase(foundEntry);
                }
            }
        };

        std::vector<std::unique_ptr<bucketTyoe> > buckets;
        hash hasher;

        bucketTyoe& get_bucket(const key& ky) const {
            const std::size_t bucketIndex = hasher(ky) % buckets.size();
            return *buckets[bucketIndex];
        }
    public:
        typedef key keyType; 
        typedef value valueType; 
        typedef hash hashType; 
        
        Threadsafe_LookupTable(unsigned num_buckets = 19, 
                               const hash& hasher_ = hash()):
                               buckets(num_buckets), hasher(hasher_) 
        {
            for(unsigned i = 0; i < num_buckets; ++i)
            {
                buckets[i].reset(new bucketTyoe);                            
            }
        }

        Threadsafe_LookupTable(const Threadsafe_LookupTable& other) = delete;
        Threadsafe_LookupTable& operator=(const Threadsafe_LookupTable& other) =delete;

        value value_for(const key& ky, const value& defaultVal = value()) const {
            return get_bucket(ky).value_for(ky, defaultVal);
        }

        void add_or_update_mapping(const key& ky, const value& val) {
            return get_bucket(ky).add_or_update_mapping(ky, val);
        }

        void remove_mapping(const key& ky) {
            return get_bucket(ky).remove_mapping(ky);
        }

		std::map<key, value> get_map() const {
			std::vector<std::unique_lock<boost::shared_mutex> > locks;
			for (unsigned i = 0; i < buckets.size(); ++i)
			{
				locks.push_back(std::unique_lock<boost::shared_mutex>(buckets[i]->get_mutex()));
			}
			std::map<key, value> res;
			for (unsigned i = 0; i < buckets.size(); ++i)
 			{
				for (bucketTyoe::bucketIterator it = buckets[i]->get_data().begin();
					 it != buckets[i]->get_data().end();
					 ++it)
				{
					res.insert(*it);
				}
			}
			return res;
		}
    };
}
#endif