try:
    import os
    import json
    from typing import Union
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

def remove_course_from_major(major_name: str, course_name: str):
    major_data = get_major_data(major_name)

    if not check_major_structure(major_data):
        raise ValueError("Invalid major structure")

    remove_course_recursive(major_data["requisitos"]["subrequisitos"], course_name)

    update_major_data(major_name, major_data)

def remove_course_recursive(subrequisitos, course_name):
    if isinstance(subrequisitos, list):
        for item in subrequisitos:
            if isinstance(item, dict) and "subrequisitos" in item:
                remove_course_recursive(item["subrequisitos"], course_name)
            elif isinstance(item, str) and item == course_name:
                subrequisitos.remove(item)


def get_major_data(major: str):
    path = f'{os.getcwd()}/data/majors/{major}.json'
    try:
        with open(path, encoding='utf-8', mode='r') as major_file:
            major_data = json.load(major_file)
    except Exception as e:
        raise ValueError(f"Failed to load major data: {e}")
    return major_data

def update_major_data(major: str, data):
    path = f'{os.getcwd()}/data/majors/{major}.json'
    try:
        print(f'New Data: {data}')
        with open(path, encoding='utf-8', mode='w') as major_file:
            json.dump(data, major_file, indent=4)
    except Exception as e:
        raise ValueError(f"Failed to update major data: {e}")

def check_major_structure(major: Union[str, dict]):
    if type(major) is str:
        major_data = get_major_data(major)
    else:
        major_data = major

    # Main Major Structure
    return checker_dfs(major_data)

def checker_dfs(data, depth=0):
    # First we check if the keys structure is correct
    if type(data) is dict:
        # We check if it's a major or a track
        key = 'requisitos'
        if key not in data.keys():
            key = 'subrequisitos'
        elif key not in data.keys():
            return False
        
        # We check the other keys
        if key == 'requisitos' and 'nombre' not in data.keys():
            return False
        elif key == 'subrequisitos':
            # We check name tag in depth 2, we could check in dept 3, but 
            # it can either be or not be in it, so we do not need to
            # check it
            if depth == 2:
                if 'relacion' not in data.keys() or 'nombre' not in data.keys():
                    return False
            elif 'relacion' not in data.keys():
                return False

        sub_data = data[key]
    
    # Next we check if the values structure is correct
    elif type(data) is str:
        return True
    else:
        return False
    
    depth += 1

    if type(sub_data) is dict:
        return checker_dfs(sub_data, depth)
    elif type(sub_data) is list:
        if len(sub_data) == 0:
            return False
        checks = []
        for char in sub_data:
            checks.append(checker_dfs(char, depth=depth))
        if all(checks):
            return True
        else:
            return False
    elif type(sub_data) is str:
        return True
    else:
        return False

def get_all_majors():
    for _, _, files in os.walk(f'{os.getcwd()}/majors'):
        majors = list(filter(lambda char: '.json' in char, files))
        majors = list(map(lambda char: char.split('.')[0], majors))
        return majors

def get_all_packages(major_name: str):
    major_data = get_major_data(major_name)
    major = {
        'name' : major_data['nombre'],
        'packages' : []
    }
    return packages_builder(major, major_data['requisitos'], None)

def major_builder(major, data, relation):
    for char in data:
        pack = {
            'name' : char['nombre'],
            'courses' : {
                'AND' : [],
                'OR' : [],
            }
        }
        relation = char['relacion']
        pack = packages_builder(pack, char, relation)
        major['packages'].append(pack)
    
    return major

def packages_builder(pack, data, relation):
    if type(data) is dict:
        key = 'subrequisitos'
        sub_data = data[key]
        relation = data['relacion']
        if type(sub_data) is list:
            major_checker = [type(elem) is dict for elem in sub_data]
            if all(major_checker):
                pack = {
                    'name' : pack['name'],
                    'packages' : []
                }
                return major_builder(pack, sub_data, relation)
            else:
                for char in sub_data:
                    if char not in ['AND', 'OR']:
                        if type(char) is dict:
                            if 'nombre' in char:
                                pack = {
                                    'name' : char['nombre'],
                                    'courses' : {
                                        'AND' : [],
                                        'OR' : [],
                                    }
                                }
                                relation = char['relacion']
                        val = packages_builder(pack, char, relation)
        return pack
    elif type(data) is str:
        if data not in ['AND', 'OR']:
            pack['courses'][relation].append(data)

def check_major(major_name, courses):
    # I know that this logic can be segmented better, but it is currenlty
    # 2 am and I am tired
    major = get_all_packages(major_name)
    major['approved'] = False
    for package in major['packages']:
        package['approved'] = False
        if package['name'] != 'Track':
            package['OG_ORs'] = len(package['courses']['OR'])
            for course in courses:
                if course in package['courses']['AND']:
                    package['courses']['AND'].remove(course)
                if course in package['courses']['OR']:
                    package['courses']['OR'].remove(course)
            if len(package['courses']['AND']) == 0:
                if len(package['courses']['OR']) == 0:
                    package['approved'] = True
                elif len(package['courses']['OR']) < package['OG_ORs']:
                    package['approved'] = True
        else:
            for sub_package in package['packages']:
                sub_package['approved'] = False
                sub_package['OG_ORs'] = len(sub_package['courses']['OR'])
                for course in courses:
                    if course in sub_package['courses']['AND']:
                        sub_package['courses']['AND'].remove(course)
                    if course in sub_package['courses']['OR']:
                        sub_package['courses']['OR'].remove(course)
                if len(sub_package['courses']['AND']) == 0:
                    if len(sub_package['courses']['OR']) == 0:
                        sub_package['approved'] = True
                    elif len(sub_package['courses']['OR']) < sub_package['OG_ORs']:
                        sub_package['approved'] = True
            if any([char['approved'] for char in package['packages']]):
                package['approved'] = True
    if all([char['approved'] for char in  major['packages']]):
        major['approved'] = True
    return major['approved']           


if __name__ == '__main__':
    # print(check_major_structure('software'))
    print(get_all_majors())
    courses = [
        "MAT1610",
        "FIS1514",
        "IIQ1003",
        "ICE2006",
        "IIC2133",
        "IIC2413",
        "IIC2154",
        "IBM1005",
        "IIC1253",
        "VRA4000",
        "VRA1323"
    ]
    print('COMPU')
    print(check_major('compu', courses))
    

    print('SOFTWARE')
    print(check_major('software', courses))