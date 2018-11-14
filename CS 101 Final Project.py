example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

def get_snippets_list(string_input):
    return string_input.split(".")

def get_user(string_input):
    if " is connected to" in string_input:
        end = string_input.find(" is connected to")
        return string_input[ : end]
    elif " likes to play " in string_input:
        end = string_input.find(" likes to play ")
        return string_input[ : end]

def get_friends_list(string_input):
    start = string_input.find(" is connected to ")
    n = len(" is connected to ")
    #end = string_input.find(".", start)
    friends_str = string_input[start + n : ]
    new_str = ""
    for i in friends_str:
        if i == ",":
            new_str += " "
        else:
            new_str += i
    return new_str.split()

def get_games_list(string_input):
    start = string_input.find(" likes to play ")
    n = len(" likes to play ")
    #end = string_input.find(".", start + 1)
    games_str = string_input[start + n : ]
    list_of_games = []
    game = ""
    for i in games_str:
        if i != ",": #and i != ".":
            game += i
        else:
            list_of_games.append(game)
            game = ""
    list_of_games.append(game)
    games_list = []
    for g in list_of_games:
        if g[0] == " ":
            games_list.append(g[1 : ])
        else:
            games_list.append(g)
    return games_list

def create_data_structure(string_input):
    network = {}
    snippets_list = get_snippets_list(string_input)
    i = 0
    while i < len(snippets_list):
        if i % 2 == 0:
            friends = get_friends_list(snippets_list[i])
            i += 1
        else:
            games = get_games_list(snippets_list[i])
            user = get_user(snippets_list[i])
            network[user] = friends, games
            i += 1
    return network

net = create_data_structure(example_input)
#print net
#>>> {'Freda': (['Olive', 'John', 'Debra'], ['Starfleet Commander', 'Ninja Hamsters', 'Seahorse Adventures']), 'Ollie': (['Mercedes', 'Freda', 'Bryant'], ['Call of Arms', 'Dwarves and Swords', 'The Movie: The Game']), 'Debra': (['Walter', 'Levi', 'Jennie', 'Robin'], ['Seven Schemers', 'Pirates in Java Island', 'Dwarves and Swords']), 'Olive': (['John', 'Ollie'], ['The Legend of Corgi', 'Starfleet Commander']), 'Levi': (['Ollie', 'John', 'Walter'], ['The Legend of Corgi', 'Seven Schemers', 'City Comptroller: The Fiscal Dilemma']), 'Jennie': (['Levi', 'John', 'Freda', 'Robin'], ['Super Mushroom Man', 'Dinosaur Diner', 'Call of Arms']), 'Mercedes': (['Walter', 'Robin', 'Bryant'], ['The Legend of Corgi', 'Pirates in Java Island', 'Seahorse Adventures']), 'John': (['Bryant', 'Debra', 'Walter'], ['The Movie: The Game', 'The Legend of Corgi', 'Dinosaur Diner']), 'Robin': (['Ollie'], ['Call of Arms', 'Dwarves and Swords']), 'Bryant': (['Olive', 'Ollie', 'Freda', 'Mercedes'], ['City Comptroller: The Fiscal Dilemma', 'Super Mushroom Man']), 'Walter': (['John', 'Levi', 'Bryant'], ['Seahorse Adventures', 'Ninja Hamsters', 'Super Mushroom Man'])}

def get_connections(network, user):
    if user not in network:
        return None
    elif network[user][0] == []:
        return []
    else:
        return network[user][0]

def get_games_liked(network,user):
    if user not in network:
        return None
    elif network[user][1] == []:
        return []
    else:
        return network[user][1]

def add_connection(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    elif user_B in network[user_A][0]:
        return network
    else:
        network[user_A][0].append(user_B)
        return network

def add_new_user(network, user, games):
    if user in network:
        return network
    else:
        network[user] = [], games
        return network

def get_secondary_connections(network, user):
    if user not in network:
        return None
    elif network[user][0] == []:
        return []
    sec_degrees = []
    for friend in network[user][0]:
        for connection in network[friend][0]:
            if connection not in sec_degrees:
                sec_degrees.append(connection)
    return sec_degrees

def count_common_connections(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    else:
        count = 0
        for friend in network[user_A][0]:
            for connection in network[user_B][0]:
                if connection == friend:
                    count += 1
        return count

def find_path_to_friend(network, user_A, user_B, viewed=None):
    if viewed==None:
        viewed=[]
    if user_A not in network or user_B not in network:
        return None
    else:
        connected = get_connections(network, user_A)
        if user_B in connected:
            return [user_A, user_B]
        else:
            viewed.append(user_A)
            for each in connected:
                if each not in viewed:
                    path = find_path_to_friend(network, each, user_B, viewed)
                    if path:
                        return [user_A] + path
            return None


print net
#print find_path_to_friend(net, "John", "Olive", viewed=None)
