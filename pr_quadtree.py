

class quadtree_node:
    
    '''
    Working to add capacity attribute
    value will now be a list of values, coordinates will be a list of tuples
    label is used to represent the location of the node. the root is equal to 0
    '''
    def __init__(self, width: int, bottom_left: tuple, capacity: int, 
                 value:list = None, coordinates: list = None, label: int = 0):
        
        self.label = label
        self.capacity = capacity
        
        #pointers to child classes
        self.nw_child = None
        self.ne_child = None
        self.sw_child = None
        self.se_child = None

        #width of one side of the square cell
        self.width = width
        #coordinate pair that describes the lower-leftmost corner of the cell
        self.bottom_left = bottom_left
        #upper-rightmost corner
        self.upper_right = (bottom_left[0] + width, bottom_left[1] + width)
                       
        #boundaries that are used to determine if a point is in a cell
        self.x_left = bottom_left[0]
        self.y_left = bottom_left[1]
        self.x_right = self.upper_right[0]
        self.y_right = self.upper_right[1]
        
        #if there is a point located in this particular cell, its coordinates are stored
        #here
        #there can only be a value here if the cell is a full leaf node
        self.value = value
        #the tuple coordinates representing the location of the value in this cell
        self.coordinates = coordinates
        
    
    '''
    function to insert points into the pr quadtree. data should indicate the data that belongs in the
    point, and coordinates indicate the point location
    '''    
    def insert(self, data, insert_coordinates):
        
        #determine if the point lies within the cell's boundaries
        if self.point_in_cell(insert_coordinates):
            
            if self.value:
                #if the node has reached its capacity, it needs to be split up to insert new data
                #this does not handle the case where the node is internal
                if len(self.value) == self.capacity:
                    self.nw_child = quadtree_node(self.width/2, (self.x_left, self.y_left+self.width/2), self.capacity, label = 4*self.label + 2)
                    self.ne_child = quadtree_node(self.width/2, (self.x_left + self.width/2, self.y_left+ self.width/2), self.capacity, label = 4*self.label + 1)
                    self.sw_child = quadtree_node(self.width/2, (self.x_left, self.y_left), self.capacity, label = 4*self.label + 3)
                    self.se_child = quadtree_node(self.width/2, (self.x_left + self.width/2, self.y_left), self.capacity, label = 4*self.label + 4)
                    self.children = [self.ne_child, self.nw_child, self.sw_child, self.se_child]
                    
                    #storing data from the cell before clearing it out
                    original_value = self.value
                    original_coordinates = self.coordinates
                        
                    
                    #determine which child(ren) the orginal data will be inserted to
                    for child in self.children:
                        #linking back to parent node within the child instance
                        child.parent = self
                        #reinsert all points that were in the node that will now be an 
                        #internal node
                        for i in range(0, self.capacity):
                            
                            #inserts all the residual values, if they are in the new leaf
                            if child.point_in_cell(original_coordinates[i]):
                                child.insert(original_value[i], original_coordinates[i])
                        
                        #clears node out, makes it an internal node
                        if child.value:
                            self.value = None
                            self.coordinates = None
                    
                    #determine which child the new data will be inserted to
                    for child in self.children:
                        #determines if new insert point can be inserted into the new leaf
                        if child.point_in_cell(insert_coordinates):
                            return child.insert(data, insert_coordinates)                                                
    
                #handles internal nodes, which have self.value set to None
                elif self.nw_child:
                    
                    for child in self.children:
                        if child.point_in_cell(insert_coordinates):
                            return child.insert(data, insert_coordinates)
    
                #handles case where the cell is an empy leaf node. This is the ultimate destination of all inserted
                #points. additionally, points that are reinserted when cells break up go through these lines
                else:
                    
                    #value and location are added as attributes to the cell
                    if self.value:
                        self.value.append(data)
                        self.coordinates.append((insert_coordinates[0], insert_coordinates[1]))
                    else:
                        self.value = [data]
                        self.coordinates = [(insert_coordinates[0], insert_coordinates[1])]
                    #print('{} inserted in cell defined by origin {}, width {}'.format(data, self.bottom_left, self.width))
                    return True
            #handles internal nodes, which have self.value set to None
            elif self.nw_child:
                for child in self.children:
                    if child.point_in_cell(insert_coordinates):
                        return child.insert(data, insert_coordinates)

            #handles case where the cell is an empy leaf node. This is the ultimate destination of all inserted
            #points. additionally, points that are reinserted when cells break up go through these lines
            else:
                
                #value and location are added as attributes to the cell
                if self.value:
                    self.value.append(data)
                    self.coordinates.append((insert_coordinates[0], insert_coordinates[1]))
                else:
                    self.value = [data]
                    self.coordinates = [(insert_coordinates[0], insert_coordinates[1])]
                #print('{} inserted in cell defined by origin {}, width {}'.format(data, self.bottom_left, self.width))
                return True
        else:
            return False
    
    '''
    function used to delete data from the tree. requires both the value and
    its location as parameters
    '''
    def delete(self, data, del_coord):
        #check if point is in node
        if self.point_in_cell(del_coord):
            
            #case for full leaf nodes
            if self.coordinates:
                if del_coord in self.coordinates:
                    self.coordinates = [i for i in self.coordinates if i != del_coord]
                    self.value = [i for i in self.value if i != data]
                    return True
                else:
                    return False
            
            #case for internal nodes
            else:
                if self.ne_child:
                    for child in self.children:
                        if child.delete(data, del_coord):
                            # #determines how many points there are in the current level, and
                            # #whether or not nodes need to be merged
                            # new_capacity = sum([len(i.value) for i in self.children])
                            # #working on this function now
                            # child.merge(new_capacity, self)
                            return True                      
                
                #case for empty leaf nodes 
                else:
                    return False
        else:
            return False
    
    '''
    function that merges nodes after deletions if the sum of the capacities of an internal nodes
    children do not exceed the capacity paremeter
    '''
    def merge(self, new_capacity, parent):
        if self:
            if self.children:
                new_cap = 0
                for i in self.children:
                    if i.value:
                        new_cap += len(i.value)
                if new_cap == 0:
                    pass
            if new_capacity <= parent.capacity:
                pass
            #put values from children in the parent
            parent.value = []
            parent.coordinates = []
            
            for i in parent.children:
                parent.value.append([x for x in i.value])
                parent.coordinates.append([x for x in i.coordinates])
            
            #remove pointers to children
            for i in parent.children:
                i = None
            parent.children = None
            
            return True
        else:
            return False
    '''
    using query coordinates, this function determines if the point lies
    within the node defined by self.
    if a point lies on the south or west boundary of a node, it should be considered internal
    if it lies on the north or east boundary, it should be external
    special case if it has an x or y coordinate that is the maximum value of the root node
    in this case that would be 512
    '''
    def point_in_cell(self, coordinates):
        
        if self.x_left <= coordinates[0] < self.x_right and self.y_left <= coordinates[1] < (self.y_right):
            return True
        #handling edge cases where point lies on the north or east boundaries of the domain
        else:
            if self.label == 0:
                if self.x_left <= coordinates[0] <= self.x_right and self.y_left <= coordinates[1] <= (self.y_right):
                    return True
                else:
                    return False
            else:

                label = self.label -1
                #calculates the width of the root node based on the label of the node
                root_width = int(self.width * (2 + (label**0.25)//1))
                print(self.label, root_width, (label**0.25)//1)
                if self.x_right == root_width and self.y_right == root_width:
                    if self.x_left <= coordinates[0] <= self.x_right and self.y_left <= coordinates[1] <= (self.y_right):
                        return True
                    else:
                        return False
                elif self.x_right == root_width:
                    if self.x_left <= coordinates[0] <= self.x_right and self.y_left <= coordinates[1] < (self.y_right):
                        return True
                    else:
                        return False
                elif self.y_right == root_width:
                    if self.x_left <= coordinates[0] < self.x_right and self.y_left <= coordinates[1] <= (self.y_right):
                        return True
                    else:
                        return False
                else:
                    return False
                
    '''
    function that is used to perform a preorder traversal on the nodes
    it prints out the label of the node
    '''
    def preorder_traversal(self):
        #checks if node exists
        if self:
            #checks if node is internal. if it is, it recursively traverses the children
            if self.ne_child:
                for i in self.children:
                    i.preorder_traversal()
                node_type = 'Internal node'
                #prints out label and value for the node. internal nodes have no value
                print(self.label, node_type)
            
            #different print statements for leaf nodes
            else:
                if self.value:
                    node_type = 'Full leaf'
                    print(self.label, node_type, len(self.value), self.value)
                else:
                    node_type = 'Empty leaf'
                    print(self.label, node_type)
     
    '''
    function to determine if a queried point is in the PR quadtree.
    query_coord should be a tuple of two numbers
    '''
    def point_query(self, query_coord):
        if self:
            
            print('SEARCH NODE {}'.format(self.label))
            if self.point_in_cell(query_coord):
                
                #if leaf node, check if the point is present
                if self.coordinates:
                    for i in range(0, len(self.coordinates)):
                        if query_coord == self.coordinates[i]:
                            print('EQUAL TO ' + str(self.value[i]))
                            return True
                    if query_coord not in self.coordinates:
                        print('NOT FOUND')
                        return False
        
                #if internal node, check the child that the point would be in
                elif self.ne_child:
                    for child in self.children:
                        if child.point_in_cell(query_coord):
                            return child.point_query(query_coord)
                #empty leaf node
                else:
                    print('NOT FOUND')
                    return False
            #query_coord is not contained by root node of the tree
            else:
                print('NOT FOUND')
                return False
            
        
class quadtree_root:
    
    #call this function with a defined coordinate and width to create an empy PR quadtree
    #capacity is also needed to determine how many points can exist in the node
    def __init__(self, width, left_corner, capacity):
        self.root = quadtree_node(width, left_corner, capacity)
    
    #insert tuples into the tree
    #data can be any variable
    #coordinates represent location of the tuple
    def insert(self, data, insert_coordinates):
        print('INSERT {} {}'.format(data, insert_coordinates))
        if self.root.insert(data, insert_coordinates):
            print('{} inserted into the PR-Quadtree'.format(data))
        else:
            print(('{} could not be inserted in the PR-Quadtree').format(data))
    
    def preorder_traversal(self):
        print('\nSTART PR')
        self.root.preorder_traversal()
        print('END PR \n')
    
    def point_query(self, query_coord):
        print('START POINT QUERY')
        self.root.point_query(query_coord)
        print('END POINT QUERY \n')
    
    def delete(self, data, del_coord):
        if self.root.delete(data, del_coord):
            #self.root.merge()
            print('{} deleted from tree at {}'.format(data, del_coord))
        else:
            print('Could not delete data at {} because it was not found'.format(del_coord))

class input_data:
    def __init__(self, filepath):
        self.filepath = filepath
        fileobj = open(self.filepath, 'r')
        points = fileobj.readlines()[1:]
        #manipulate lines into coordinate tuples
        points_x = [float(i.split(' ')[0]) for i in points]
        points_y = [float(i.split(' ')[1][0:-1]) for i in points]
        self.points = list(zip(points_x, points_y))
   

   
tree = quadtree_root(6, (0, 0), 1)

tree.insert('lutherville', (6, 6))
tree.insert('woodlawn', (1, 2))
tree.insert('catonsville', (4, 4))
# tree.insert('rosedale', (2.5, 2.5))
# tree.insert('towson', (4, 1))
# tree.insert('baltimore', (2, 5))

# sample_data = input_data('sample_points.txt')

# for i in sample_data.points:
#     tree.insert(i)

tree.preorder_traversal()
tree.point_query((6, 6))
print(1//1)