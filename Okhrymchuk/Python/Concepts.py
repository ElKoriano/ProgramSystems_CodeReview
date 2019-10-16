import math

class Coord2D(object):

    def __init__(self, x=0, y=0):
        self.X=x
        self.Y=y

    def __str__(self):
        return "X:"+str(self.X)+" Y:"+str(self.Y)


class City(object):

    def __init__(self, coords=Coord2D(),name="Just a peace of dry land"):
        self.name=name
        self.money_dictionary={}
        self.coords=coords

    def add_coins(self, country_name, count_of_coins):
        if self.money_dictionary.get(country_name):
            self.money_dictionary[country_name]+=count_of_coins
        else:
            self.money_dictionary.update({country_name:count_of_coins})


class Countries(object):

    def __init__(self):
        self.town_list=[]
        self.country_dict={}
        self.__recur_pointer=[]

    def add_country(self,name,left_down_coords,right_up_coords,count_of_coins=1000000):
        for country in self.country_dict:
            for c in self.country_dict[country]:
                if ((c[0].X>=left_down_coords.X and c[0].X<=right_up_coords.X
                     and c[0].Y>=left_down_coords.Y and c[0].Y<=right_up_coords.Y)
                     or (c[1].X>=left_down_coords.X and c[1].X<=right_up_coords.X
                     and c[1].Y>=left_down_coords.Y and  c[1].Y<=right_up_coords.Y)):
                    print("There is a town with the same coords. It cant be. Seems bad, dear user, try again")
                    return False
        if self.country_dict.get(name):
            print("attention, this country already exist")
            self.country_dict.get(name).append([left_down_coords,right_up_coords])
        else:
            self.country_dict.update({name:[[left_down_coords,right_up_coords]]})

        y_temp=right_up_coords.Y-left_down_coords.Y
        for x in range(right_up_coords.X-left_down_coords.X+1):
            for y in range(y_temp+1):
                coord_temp=Coord2D(left_down_coords.X+x,left_down_coords.Y+y)
                self.town_list.append(City(coord_temp))
                self.town_list[len(self.town_list)-1].add_coins(name, count_of_coins)
        return True

    def __get_towns_country(self, town):
        for country in self.country_dict:
            for c in self.country_dict[country]:
                if c[0].X<=town.coords.X and c[1].X>=town.coords.X and c[1].Y>=town.coords.Y and c[0].Y<=town.coords.Y:
                    return country
        return None

    def __get_towns_country_by_town_index(self, town_index):
        for country in self.country_dict:
            for c in self.country_dict[country]:
                if (c[0].X<=self.town_list[town_index].coords.X
                    and c[1].X>=self.town_list[town_index].coords.X
                    and c[1].Y>=self.town_list[town_index].coords.Y
                    and c[0].Y<=self.town_list[town_index].coords.Y):
                    return country
        return None

    def check_rules(self):
        if len(self.town_list)==0:
            return True
        self.__recur_pointer.append(0)
        self.__recur_check_if_you_can_come_to_each_city(0)
        check = len(self.__recur_pointer)==len(self.town_list)
        self.__recur_pointer.clear()
        return check

    def __get_list_of_neighbors_indexes(self,index_of_city):
        list_of_neighbors_indexes=[]
        for c in self.town_list:
            if((math.fabs(c.coords.X-self.town_list[index_of_city].coords.X)==1
                and c.coords.Y-self.town_list[index_of_city].coords.Y==0)
                or (math.fabs(c.coords.Y-self.town_list[index_of_city].coords.Y)==1
                and c.coords.X-self.town_list[index_of_city].coords.X==0)):
                list_of_neighbors_indexes.append(self.town_list.index(c))
            if len(list_of_neighbors_indexes)==4:
                break
        return list_of_neighbors_indexes

    def __recur_check_if_you_can_come_to_each_city(self,city_index):
        temp_list=self.__get_list_of_neighbors_indexes(city_index)

        for index in temp_list:
            if self.__recur_pointer.count(index)==0:
                self.__recur_pointer.append(index)
                self.__recur_check_if_you_can_come_to_each_city(index)

    def day_step(self):
        list_of_dic_buffer=[]
        country_money_dic={}
        for country in self.country_dict:
            country_money_dic.update({country:0})
        for i in range(len(self.town_list)):
            list_of_dic_buffer.append(country_money_dic.copy())
        for town_index in range(len(self.town_list)):
            temp_index_list=self.__get_list_of_neighbors_indexes(town_index)
            for country in self.town_list[town_index].money_dictionary:
                temp=self.town_list[town_index].money_dictionary[country]//1000
                for neighbour_index in temp_index_list:
                    list_of_dic_buffer[town_index][country]-=temp
                    list_of_dic_buffer[neighbour_index][country]+=temp
        for town_index in range(len(self.town_list)):
            for country in list_of_dic_buffer[town_index]:
                self.town_list[town_index].add_coins(country,list_of_dic_buffer[town_index][country])
        return self.check_all_towns_ended()

    def check_all_towns_ended(self):
        for t in self.town_list:
            for c in self.country_dict:
                if t.money_dictionary.get(c)==None or t.money_dictionary.get(c)==0:
                    return False
        return True

    def check_all_towns_from_country_ended(self,country):
        for t in self.town_list:
            if self.__get_towns_country(t)==country:
                for c in self.country_dict:
                    if t.money_dictionary.get(c)==None or t.money_dictionary.get(c)==0:
                        return False
        return True

    def clear(self):
        self.town_list.clear()
        self.country_dict.clear()
