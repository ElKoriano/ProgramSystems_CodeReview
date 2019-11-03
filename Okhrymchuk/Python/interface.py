from Concepts import *


class Interface(object):

    def __init__(self):
        self.country_set=Countries()

    def start_work(self):
        countries=Countries()

        print("Input count of countries:")
        try:
            count_of_countries=int(input())
        except:
            print("wrong input")
            return False
        for i in range(count_of_countries):
            print("Input name and position of country:")
            country_description=str.split(input())
            try:
                if (int(country_description[1])<1 or int(country_description[1])>10
                    or int(country_description[2])<1 or int(country_description[2])>10
                    or int(country_description[3])<1 or int(country_description[3])>10
                    or int(country_description[4])<1 or int(country_description[4])>10):
                    print("wrong input, try again")
                    return False
                if not countries.add_country(country_description[0],
                                            Coord2D(int(country_description[1]),int(country_description[2])),
                                            Coord2D(int(country_description[3]),int(country_description[4]))):
                        countries.clear()
                        print("wrong input format")
                        return False
            except:
                print("wrong country input format")
                return False
        if not countries.check_rules():
            print("wrong input format")
            return False
        print("Your result:")
        iterator = 0
        end_of_country_dict={}
        while True:
            for c in countries.country_dict:
                if end_of_country_dict.get(c)==None and countries.check_all_towns_from_country_ended(c):
                    end_of_country_dict.update({c:c+" ended on the "+str(iterator)+" step"})
            if countries.check_all_towns_ended():
                print("all towns in countries ended")
                break
            countries.day_step()
            iterator+=1
        for c in end_of_country_dict:
            print(end_of_country_dict[c])
        return True
