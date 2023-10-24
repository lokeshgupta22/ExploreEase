import json
import requests
import streamlit as st


def input_locations():
    graph = []
    ch = True
    while ch:
        inp = input("Enter Location you want to visit: ")
        graph.append(inp)
        cont = input("Do you want to add another location? (y/n): ")
        if cont == 'y':
            ch = True
        else:
            ch = False
    return graph


def make_pairs(graph):
    all = []
    for i in range(len(graph)):
        for j in range(i+1, len(graph)):
            pair = []
            pair.append(graph[i])
            pair.append(graph[j])
            all.append(pair)
    return all


def make_route(a):
    myroute = [
        {
            't': a[0]
        },
        {
            't': a[1]
        }
    ]
    return myroute


def get_distance(myroute):
    url = "https://distanceto.p.rapidapi.com/get"
    jsonroute = json.dumps(myroute, separators=(',', ':'))
    querystring = {"route": jsonroute}

    headers = {
        "X-RapidAPI-Key": "c129526652msh5a1f38966b3d5d1p1148fdjsn4718df801cc0",
        "X-RapidAPI-Host": "distanceto.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def make_graph(graph):
    allpairs = make_pairs(graph)
    final_graph = {}
    for i in allpairs:
        # print(i)
        myroute = make_route(i)
        final_json = get_distance(myroute)
        final_graph[str(i[0]+i[1])] = int(
            final_json['steps'][0]['distance']['haversine'])
    return final_graph


def algorithm(graph):
    src = graph[0]
    dest = graph[-1]
    visited = []
    visitedDist = []
    visited.append(src)
    visitedDist.append(0)
    savemoney = make_graph(graph)
    allplaces = list(savemoney.keys())
    alldist = list(savemoney.values())
    for j in range(len(graph)-2):
        temp = []
        for i in allplaces:
            if (src in i) and (dest not in i) and (savemoney[i] not in visitedDist):
                temp.append(savemoney[i])
        next = allplaces[alldist.index(min(temp))]
        next = next.replace(src, "")
        visited.append(next)
        visitedDist.append(min(temp))
        src = next

    visited.append(dest)
    return visited


def get_url(path):
    url = "https://www.google.com/maps/dir/"
    for i in path:
        url += (f"{i}/")
    return url


num = st.text_input('Insert number of cities to be visited')
try:
    num=int(num)
except:
    st.write('Now')

dis=[]
if st.button('next'):
    for i in range(num):
        dis.append(st.text_input(f'City {i}'))


# graph = input_locations()
# # graph = ['Mumbai', 'Manali', 'Rishikesh']
# path = algorithm(graph)
# print(path)
# print(get_url(path))
