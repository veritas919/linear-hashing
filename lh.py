# from . import Bucket 
import copy 
import math 

class LinearHashing:

    # constructor
    def __init__(self, page_size=None, policy = 0, max_overflow = 0, size_limit = 1.0):
        

        # basic error checking 
        if page_size < 0 or None:
            print("invalid page size. exitting.")
            quit()

        if policy not in range(0,4):
            print("invalid policy number. exitting.")
            quit() 
        if size_limit < 0 or size_limit > 1:
            print("size_limit should be in [0,1]")    
            quit()    
        
        self.page_size = page_size
        self.policy = policy
        self.level = 0
        self.ptr = 0
        self.is_an_overflow_rn = False
        self.num_buckets_overflowing = 0
        self.num_buckets = 1 # only keeping track of main buckets rn....NOT overflow 
        self.max_overflow = max_overflow 
        self.size_limit = size_limit 

        print("SIZELIMIT", self.size_limit)

        self.hash_table = {}
        self.hash_table [0] = []

    def insert(self, number):
        if self.policy == 0:
            self.case_0_insert(number)
        elif self.policy == 1:
            self.case_1_insert(number) 
        elif self.policy == 2:
            self.case_2_insert(number) 
        elif self.policy == 3:
            self.case_3_insert(number)
        else:
            print("invalid value for policy.")

    ######################################################################### CASE 0 INSERT ##########################################################################
    def case_0_insert(self, num):
        split_occured = False
        print("in case 0")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
            # check if any bucket is overflowing 
            #self.isOverflowedRightNow(0) 
                # if there is an overflow  ----- > create new bucket, rehash, level up, reset ptr 
            if self.isOverflowedRightNow(0) == True:  
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
                    # print(item)
                    if item % 2 == 0:
                        bucket_0.append(item)
                    else:
                        bucket_1.append(item) 
                self.hash_table[0] = bucket_0
                self.hash_table[1] = bucket_1 
                self.level = 1
                self.ptr = 0 
                self.num_buckets += 1
                split_occured = True 

                # self.isOverflowedRightNow()   # MUST RECHECK    WORKS FINE WITHOUT @@@@@@@@@@@@ TAKE OUT TEMP 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            bucket_key = None 
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                    bucket_key = ht_index_try_1
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num)
                    bucket_key = int(bigger_last_bits,2)
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                    bucket_key = int(smaller_last_bits,2)
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            # self.isOverflowedRightNow()

            # print("is overflow?", self.is_an_overflow_rn)
            # if there is an overflow  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.isOverflowedRightNow(bucket_key) == True:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("spliting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    # print("item in splitting bucket...",item)
                    item_as_bin = bin(item)[2:]

                    if len(item_as_bin) <= self.level + 1:
                        k_bits_as_int = item 
                    else:
                        k_bits_as_int = int(item_as_bin[-1: -(self.level + 2) : -1][::-1], 2)
                    
                    if k_bits_as_int == new_bucket_value_0:
                        bucket_0.append(item)
                    elif k_bits_as_int == new_bucket_value_1:
                        bucket_1.append(item)
                    else:
                        print("problemo. item val is: ", item) 

                self.hash_table[new_bucket_value_0] = bucket_0
                self.hash_table[new_bucket_value_1] = bucket_1 
                
                self.num_buckets += 1
                self.ptr +=1 
                split_occured = True 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

                # self.isOverflowedRightNow() # RECHECK...MUST DO        WORKS FINE WITHOUT  @@@@@@@@@@@@@@@@@@@@@@ TAKE OUT 
        return split_occured 

    ##################################################################### CASE 1 INSERT ####################################################

    def case_1_insert(self, num):
        split_occured = False
        print("in case 1")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 

            # if the number of overflow buckets is >= max_overflow  ----- > create new bucket, rehash, level up, reset ptr 
            if self.get_total_number_of_overflow_buckets() >=  self.max_overflow:  
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
                    # print(item)
                    if item % 2 == 0:
                        bucket_0.append(item)
                    else:
                        bucket_1.append(item) 

                self.hash_table[0] = bucket_0
                self.hash_table[1] = bucket_1 

                self.level = 1
                self.ptr = 0 
                self.num_buckets += 1 # dont know abt this 
                split_occured = True 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num) 
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            #self.isOverflowedRightNow()

            #print("is overflow?", self.is_an_overflow_rn)
            # if the number of overflow buckets is >= maxoverflow  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.get_total_number_of_overflow_buckets() >= self.max_overflow:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("splitting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    #print("item in splitting bucket...",item)
                    item_as_bin = bin(item)[2:]

                    if len(item_as_bin) <= self.level + 1:
                        k_bits_as_int = item 
                    else:
                        k_bits_as_int = int(item_as_bin[-1: -(self.level + 2) : -1][::-1], 2)
                    
                    if k_bits_as_int == new_bucket_value_0:
                        bucket_0.append(item)
                    elif k_bits_as_int == new_bucket_value_1:
                        bucket_1.append(item)
                    else:
                        print("problemo. item val is: ", item) 

                self.hash_table[new_bucket_value_0] = bucket_0
                self.hash_table[new_bucket_value_1] = bucket_1 
                
                self.num_buckets += 1
                self.ptr +=1 
                split_occured = True 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

        return split_occured 

######################################################################### CASE 2 ############################################################# 

    def case_2_insert(self, num):
        split_occured = False
        print("in case 2")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 

            # if the number of overflow buckets is >= size_limit  ----- > create new bucket, rehash, level up, reset ptr 
            if self.get_current_capacity_ratio() >=  self.size_limit:  
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
                    # print(item)
                    if item % 2 == 0:
                        bucket_0.append(item)
                    else:
                        bucket_1.append(item) 

                self.hash_table[0] = bucket_0
                self.hash_table[1] = bucket_1 

                self.level = 1
                self.ptr = 0 
                self.num_buckets += 1 # dont know abt this 
                split_occured = True 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num) 
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            # if the current capacity is >= size_limit  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.get_current_capacity_ratio() >= self.size_limit:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("splitting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    #print("item in splitting bucket...",item)
                    item_as_bin = bin(item)[2:]

                    if len(item_as_bin) <= self.level + 1:
                        k_bits_as_int = item 
                    else:
                        k_bits_as_int = int(item_as_bin[-1: -(self.level + 2) : -1][::-1], 2)
                    
                    if k_bits_as_int == new_bucket_value_0:
                        bucket_0.append(item)
                    elif k_bits_as_int == new_bucket_value_1:
                        bucket_1.append(item)
                    else:
                        print("problemo. item val is: ", item) 

                self.hash_table[new_bucket_value_0] = bucket_0
                self.hash_table[new_bucket_value_1] = bucket_1 
                
                self.num_buckets += 1
                self.ptr +=1 
                split_occured = True 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

        return split_occured 


############################################################################### CASE 3 ##############################################################

    def case_3_insert(self, num):
        split_occured = False
        print("in case 3")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
            # if there is an overflow for bucket that would be split  ----- > create new bucket, rehash, level up, reset ptr 
            if self.isOverflowedRightNow(self.ptr) == True:  
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
                    # print(item)
                    if item % 2 == 0:
                        bucket_0.append(item)
                    else:
                        bucket_1.append(item) 
                self.hash_table[0] = bucket_0
                self.hash_table[1] = bucket_1 
                self.level = 1
                self.ptr = 0 
                self.num_buckets += 1
                split_occured = True 

                # self.isOverflowedRightNow()   # MUST RECHECK    WORKS FINE WITHOUT @@@@@@@@@@@@ TAKE OUT TEMP 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            bucket_key = None 
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                    bucket_key = ht_index_try_1
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num)
                    bucket_key = int(bigger_last_bits,2)
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                    bucket_key = int(smaller_last_bits,2)
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            # if there is an overflow for bucket that would be split ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.isOverflowedRightNow(self.ptr) == True:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("spliting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    # print("item in splitting bucket...",item)
                    item_as_bin = bin(item)[2:]

                    if len(item_as_bin) <= self.level + 1:
                        k_bits_as_int = item 
                    else:
                        k_bits_as_int = int(item_as_bin[-1: -(self.level + 2) : -1][::-1], 2)
                    
                    if k_bits_as_int == new_bucket_value_0:
                        bucket_0.append(item)
                    elif k_bits_as_int == new_bucket_value_1:
                        bucket_1.append(item)
                    else:
                        print("problemo. item val is: ", item) 

                self.hash_table[new_bucket_value_0] = bucket_0
                self.hash_table[new_bucket_value_1] = bucket_1 
                
                self.num_buckets += 1
                self.ptr +=1 
                split_occured = True 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0
 
        return split_occured 


    ############################################################## Print to console method #######################################################

    def print(self):        
        for key in self.hash_table:
            key_binary = bin(key)[2:]
            print("key", key, end = " binary ")
            if (key + (2**(self.level)) in self.hash_table):
                keyStr = key_binary.zfill(self.level + 1)
            else:
                keyStr = key_binary.zfill(self.level)
            print(keyStr, end = " : ")

            count = 0
            for i, item in enumerate(self.hash_table[key]):
                print(item, end = " ") 
                count += 1
                if count == self.page_size and i != len(self.hash_table[key]) - 1:
                    print(" --  ", end = "")
                    count = 0
            print("\n")
        print("Level", self.level)
        print("Ptr", self.ptr)

    # use for Case 2 
    def get_current_capacity_ratio(self):
        # get number of items in the table
        num_items_in_table = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            num_items_in_table += num_items_for_key
        
        # get number of pages in table
        page_number = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0: ####################################### if no numbers in key, assume it still starts with 1 page ????????????????? VERIFY THIS 
                page_number += 1
            else:
                page_number += int(math.ceil(num_items_for_key / self.page_size)) 

        current_capacity = (num_items_in_table) / (page_number * self.page_size)
        return current_capacity          

        
    def get_num_buckets(self):
        return self.num_buckets 

    def isOverflowedRightNow(self, bucket_key):
        if bucket_key not in self.hash_table:
            print("error...key not in table. can't check for overflow")
        else:
            if len(self.hash_table[bucket_key]) > self.page_size: #overrflow!)
                return True 
            else:
                return False 
            
        '''
        flag = False 
        for key in self.hash_table:
                if len(self.hash_table[key]) > self.page_size: #overrflow!
                    self.is_an_overflow_rn = True
                    flag = True
        if flag == True:
            self.is_an_overflow_rn = True
        else:
            self.is_an_overflow_rn = False 

        '''

    def get_total_number_of_overflow_buckets(self):
        num_overflow = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0:
                continue
            overflow_for_that_key = int(math.ceil(num_items_for_key / self.page_size)) - 1
            num_overflow += overflow_for_that_key 

        print("num overflow: ", num_overflow)
        return num_overflow 




    def print_ht(self):
        for key in self.hash_table:
            print("key", key, end = " : ")
            for item in self.hash_table[key]:
                print(item, end = " ") 
            print("\n")

if __name__ == "__main__":
    # x = LinearHashing(page_size = 2, policy = 0, max_overflow = 2)
    # x = LinearHashing(page_size = 2, policy = 1, max_overflow = 0) # should function same as default case 
    # x = LinearHashing(page_size = 2, policy = 2, size_limit = 0.7)
    x = LinearHashing(page_size = 2, policy = 3)

    x.insert(2)
    x.insert(0)
    x.insert(1) 
    print("bucket #: ", x.get_num_buckets())
    x.insert(5)
    print("bucket #: ", x.get_num_buckets())
    x.insert(23)
    print("bucket #: ", x.get_num_buckets())
    x.insert(42)
    print("bucket #: ", x.get_num_buckets())
    x.insert(55)
    print("bucket #: ", x.get_num_buckets())
    x.insert(10)
    print("bucket #: ", x.get_num_buckets())
    x.print_ht()
    x.insert(999)
    x.insert(-13)
    x.insert(-55)

    # x.print_ht() 
    x.insert(43) 

    x.print_ht() 
    
    x.insert(45)
    x.insert(2328356)
    x.insert(8) 
    x.insert(21)
    x.insert(32)
    x.insert(2000)
    x.insert(0)
    x.insert(1) 


    x.print_ht()
    print(" about to print in binary.........")
    x.print() 

