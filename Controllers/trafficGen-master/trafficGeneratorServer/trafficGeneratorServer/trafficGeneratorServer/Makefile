EXEC		=	server
##LIB_OPTS 	=	-I /home/mininet/boost_1_61_0/Suraj_ScalableSDN/include -L/home/mininet/boost_1_61_0/Suraj_ScalableSDN/lib
LIB_OPTS 	=	-I $(BOOST_ROOT)
BOOST_OPTS	=	-lboost_program_options -lboost_system
CPPFLAGS	= 	-pthread -g -Wall -std=gnu++11
CXX			=	g++
SRC_FILES	=	main.cpp
#$CXX -std=gnu++11 -Wall  -g -pthread -o server main.cpp -I /usr/local/Cellar/boost/1.56.0/include
all:
	$(CXX) $(CPPFLAGS) $(SRC_FILES) $(BOOST_OPTS) -o $(EXEC) $(LIB_OPTS)
clean:
	$(RM) $(EXEC)
