import json
import requests
import streamlit as st
import webbrowser


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
        "X-RapidAPI-Key": "fb2a71e4bcmsh4200c850939add6p19f078jsn2c9524f86e8d",
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
    if graph:
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
    if path:
        for i in path:
            url += (f"{i}/")
        return url


def streamlit_input():
    st.title("Plan Your Trip !!!")

    locations = []
    num_locations = st.number_input(
        "Enter Number of Locations", min_value=1, value=1)

    for i in range(num_locations):
        if i == 0:
            locations.append(st.text_input(f"Source Location"))
        elif i == num_locations - 1:
            locations.append(st.text_input(f"Destination Location"))
        else:
            locations.append(st.text_input(f"Location {i+1}"))

    if st.button("Calculate Best Route"):
        algorithm(locations)


# graph = input_locations()
graph = streamlit_input()
path = algorithm(graph)
url = get_url(path)

if path:
    result = ''
    for place in path:

        result += place
        if place != path[-1]:
            result += ' >> '

    st.write(result)

    st.markdown(f'<a href="{url}" target="_blank">Show route on Google Maps</a>',
                unsafe_allow_html=True)
