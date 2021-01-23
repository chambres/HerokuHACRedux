import re


grade = {}


def get_number(local_result):
    return re.findall("\d+\.\d+", local_result)[0]



def find_name(element):
    heading = element.findAll("a", {"class": "sg-header-heading"}) #sg-header-heading"

    name_with_whitespace = re.findall(r"(?s)(?<=\>)(.*?)(?=\<\/a\>)", str(heading))[0] #extracting name with lots of whitespace
    
    name = str(re.sub(r'\s{2,}',' ', name_with_whitespace)).lstrip() #a lot of bullshit to extract the name, should fix with regex 

    return name
    
    
def find_total_avg(element):
    #grade[total_average] = re.findall('(\d+)', str(element.findAll("span", {"class": "sg-header-heading"})))
    return re.findall('(\d+)', str(element.findAll("span", {"class": "sg-header-heading"}))) #extracts avg
    
    
    
def get_grid(classes):


    results = re.findall(r'(?s)(?<=\<td)(.*?)(?=\<\/td\>)', str(classes))

    date_due = re.findall(r'\d{2}\/\d{2}\/\d{4}', results[0])[0]
    
    try:
    
        date_assigned = re.findall(r'\d{2}\/\d{2}\/\d{4}', results[1])[0]
    except IndexError:
        date_assigned = ""
        



    various_things = list(filter(None, results[2].split("\n"))) #removes bullshit            
    
    try:
        title_of_assignment = str(re.findall(r'(?<=Classwork\: ).*', str(various_things[2]))[0])
    except: 
        title_of_assignment = ""
    
    try:
        type_of_grade = re.findall(r'(?<=Category\: ).*', str(various_things[3]))[0]
    except: 
        type_of_grade = ""
        
    try:    
        due_date = re.findall(r'(?<=Due Date\: ).*', str(various_things[4]))[0]
    except:
        due_date = ""
        
    try:
        max_points = re.findall(r'(?<=Max Points\: ).*', str(various_things[5]))[0]
    except:
        max_points = ""
        
    try:    
        can_be_dropped = re.findall(r'(?<=Can Be Dropped\: ).*', str(various_things[6]))[0] #dunno what this does, but kept it for completions sake
    except: 
        can_be_dropped = ""

    try:
        score = get_number(results[4]) #actual grade
    except: 
        score = ""
    try:   
        total_points = get_number(results[5])
    except: 
        total_points = ""
        
    try:    
        weight = get_number(results[6])
    except: 
        weight = ""
    
    try:    
        weighted_score = get_number(results[7])
    except: 
        weighted_score = ""
        
    try:   
        weighted_total_points = get_number(results[8])
    except:
        weighted_total_points = ""
    
    try:
        percentage = get_number(results[9]) 
    except:
        percentage = ""
        

    temporary =           {
                            title_of_assignment: {
                                  'score': score,
                                  'date_due': date_due,
                                  'date_assigned': date_assigned,
                                  'title_of_assignment': title_of_assignment,
                                  'type_of_grade': type_of_grade,
                                  'due_date': due_date,
                                  'max_points': max_points, 
                                  'can_be_dropped': can_be_dropped,
                                  'total_points': total_points, #pretty sure this is the same as 'score' 
                                  'weight': weight,
                                  'weighted_score': weighted_score,
                                  'weighted_total_points': weighted_total_points,
                                  'percentage': percentage                                  
                                  }
                          }

    return temporary
            


def main(classes):
    

    grades = {}
    for class_ in classes: #like, alg2, chem, etc etc
 
        name = find_name(class_)                                                        
        grid = class_.findAll("table", {"class": "sg-asp-table"}) #grid
        
        
        try: 
            assignments = grid[0].findAll("tr", {"class": "sg-asp-table-data-row"}) #every assignment 
            #del grid[-1]                                                   #idk what this does, but it doesnt break it, so why not??             
        
            grades[name] = {"average": find_total_avg(class_)[1]}
                
            for assignment in assignments:
                try:
                    a = get_grid(assignment)
                    grades[name].update(**a)
                    
                except IndexError: #it tries to parse the major minor and other averages, that dont match the normal logic, so it errors out, i need to fix this
                    pass
        except IndexError:
            grades[name] = {}
            
    return grades
    




