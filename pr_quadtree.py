import matplotlib.pyplot as plt

class quadtree_node:
    
    '''
    Working to add capacity attribute
    value will now be a list of values, coordinates will be a list of tuples
    label is used to represent the location of the node. the root is equal to 0
    '''
    def __init__(self, width: int, bottom_left: tuple, capacity: int, 
                 coordinates: list = None, label: int = 0):
        
        self.label = label
        self.capacity = capacity
        
        #pointers to child classes
        self.nw_child = None
        self.ne_child = None
        self.sw_child = None
        self.se_child = None
        #root node will never have a parent
        self.parent = None
        
        #width of one side of the square cell
        self.width = width
        #accessed to handle edge cases for points lying on the border of the root node
        self.root_width = width

           
        #boundaries that are used to determine if a point is in a cell
        self.x_left = bottom_left[0]
        self.y_left = bottom_left[1]
        self.x_right = bottom_left[0] + width
        self.y_right = bottom_left[1] + width
        

        #the tuple coordinates representing the location(s) of the value(s) in this cell
        self.coordinates = coordinates
        
    
    '''
    function to insert points into the pr quadtree. data should indicate the data that belongs in the
    point, and coordinates indicate the point location
    '''    
    def insert_point(self, data, insert_coordinates):
        
        #determine if the point lies within the cell's boundaries
        if self.point_in_cell(insert_coordinates):
            
            if self.coordinates:
                #if the node has reached its capacity, it needs to be split up to insert new data
                #this does not handle the case where the node is internal
                if len(self.coordinates) == self.capacity:
                    self.nw_child = quadtree_node(self.width/2, (self.x_left, self.y_left+self.width/2), self.capacity, label = 4*self.label + 2)
                    self.ne_child = quadtree_node(self.width/2, (self.x_left + self.width/2, self.y_left+ self.width/2), self.capacity, label = 4*self.label + 1)
                    self.sw_child = quadtree_node(self.width/2, (self.x_left, self.y_left), self.capacity, label = 4*self.label + 3)
                    self.se_child = quadtree_node(self.width/2, (self.x_left + self.width/2, self.y_left), self.capacity, label = 4*self.label + 4)
                    self.children = [self.ne_child, self.nw_child, self.sw_child, self.se_child]
                    
                    #storing data from the cell before clearing it out
                    original_coordinates = self.coordinates
                        
                    
                    #determine which child(ren) the orginal data will be inserted to
                    for child in self.children:
                        #linking back to parent node within the child instance
                        child.parent = self
                        child.root_width = self.root_width
                        #reinsert all points that were in the node that will now be an 
                        #internal node
                        for i in original_coordinates:
                            
                            #inserts all the residual values, if they are in the new leaf
                            if child.point_in_cell(i):
                                child.insert_point(original_coordinates[i], i)
                        
                        #clears node out, makes it an internal node
                        if child.coordinates:
                            self.coordinates = None
                    
                    #determine which child the new data will be inserted to
                    for child in self.children:
                        #determines if new insert point can be inserted into the new leaf
                        if child.point_in_cell(insert_coordinates):
                            return child.insert_point(data, insert_coordinates)                                                
    
                #handles internal nodes, which have self.value set to None
                elif self.nw_child:
                    
                    for child in self.children:
                        if child.point_in_cell(insert_coordinates):
                            return child.insert_point(data, insert_coordinates)
    
                #handles case where the cell is an empy leaf node. This is the ultimate destination of all inserted
                #points. additionally, points that are reinserted when cells break up go through these lines
                else:
                    
                    #value and location are added as attributes to the cell
                    if self.coordinates:
                        self.coordinates[insert_coordinates] = data
                    else:
                        self.coordinates = {insert_coordinates: data}
                    #print('{} inserted in cell defined by origin {}, width {}'.format(data, self.bottom_left, self.width))
                    return True
            #handles internal nodes, which have self.value set to None
            elif self.nw_child:
                for child in self.children:
                    if child.point_in_cell(insert_coordinates):
                        return child.insert_point(data, insert_coordinates)

            #handles case where the cell is an empy leaf node. This is the ultimate destination of all inserted
            #points. additionally, points that are reinserted when cells break up go through these lines
            else:    
                #value and location are added as attributes to the cell
                if self.coordinates:
                    self.coordinates[insert_coordinates] = data
                else:
                    self.coordinates = {insert_coordinates: data}
                #print('{} inserted in cell defined by origin {}, width {}'.format(data, self.bottom_left, self.width))
                return True
        else:
            return False
    
    '''
    function used to delete data from the tree. requires both the value and
    its location as parameters
    '''
    def delete(self, del_coord):
        #check if point is in node
        if self.point_in_cell(del_coord):
            
            #case for full leaf nodes
            if self.coordinates:
                if del_coord in self.coordinates:
                    #remove coordinate
                    new_coords = [i for i in self.coordinates if i != del_coord]
                    new_data = [self.coordinates[i] for i in new_coords]
                    #recreate dictionary without deleted coordinate
                    self.coordinates = dict(zip(new_coords, new_data))
                    if self.parent:
                        self.parent.merge()
                    return True
                else:
                    return False
            
            #case for internal nodes
            else:
                if self.ne_child:
                    for child in self.children:
                        if child.delete(del_coord):
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
    def merge(self):
        #variable used to check if a merge is required
        num_pts = 0
        if self.coordinates:
            num_pts += len(self.coordinates)
        
        if self.ne_child:
            for i in self.children:
                #determine how many points are in the parent node's children
                if i.coordinates:
                    num_pts += len(i.coordinates)
                elif i.ne_child:
                    for child in i.children:
                        num_pts += child.merge()

            if num_pts <= self.capacity:
                if not self.coordinates:
                    self.coordinates = {}
                for i in self.children:
                    if i.coordinates:
                        for x in i.coordinates:
                            self.coordinates[x] = i.coordinates[x]
                #remove pointers to children
                self.ne_child = None
                self.nw_child = None
                self.sw_child = None
                self.se_child = None
                self.children = None
                if self.parent:
                    self.parent.merge()
        return num_pts

        
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

                if self.x_right == self.root_width and self.y_right == self.root_width:
                    if self.x_left <= coordinates[0] <= self.x_right and self.y_left <= coordinates[1] <= (self.y_right):
                        return True
                    else:
                        return False
                elif self.x_right == self.root_width:
                    if self.x_left <= coordinates[0] <= self.x_right and self.y_left <= coordinates[1] < (self.y_right):
                        return True
                    else:
                        return False
                elif self.y_right == self.root_width:
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
                if self.coordinates:
                    node_type = 'Full leaf'
                    print(self.label, node_type, len(self.coordinates), self.coordinates)
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
                    if query_coord in self.coordinates:
                        print('EQUAL TO ' + str(self.coordinates[query_coord]))
                        return True
                    else:
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
            
    def make_plot(self):
        #checks if node exists
        if self:
            #checks if node is internal. if it is, it recursively traverses the children
            if self.ne_child:
                for i in self.children:
                    i.make_plot()

            #different print statements for leaf nodes
            else:
                if self.coordinates:
                    plt.scatter([i[0] for i in self.coordinates], [i[1] for i in self.coordinates],
                                color = '#008837', zorder = 5)
                plt.plot([self.x_left, self.x_left, self.x_right, self.x_right, self.x_left],
                         [self.y_left, self.y_right, self.y_right, self.y_left, self.y_left], 
                         color = '#7b3294')
                
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
        if self.root.insert_point(data, insert_coordinates):
            print('{} inserted into the PR-Quadtree'.format(data))
        else:
            print(('{} could not be inserted in the PR-Quadtree').format(data))
    
    def preorder_traversal(self):
        print('\nSTART PR')
        self.root.preorder_traversal()
        print('END PR \n')
    
    def point_query(self, query_coord):
        print('START POINT QUERY FOR {}'.format(query_coord))
        self.root.point_query(query_coord)
        print('END POINT QUERY \n')
    
    def delete(self, del_coord):
        if self.root.delete(del_coord):
            print('{} deleted from tree'.format(del_coord))
        else:
            print('Could not delete data at {} because it was not found'.format(del_coord))
    
    def make_plot(self):
        plt.style.use('seaborn-darkgrid')
        self.root.make_plot()
        plt.axis('scaled')
        plt.show()

class input_data:
    def __init__(self, filepath):
        self.filepath = filepath
        fileobj = open(self.filepath, 'r')
        points = fileobj.readlines()[1:]
        #manipulate lines into coordinate tuples
        points_x = [float(i.split(' ')[0]) for i in points]
        points_y = [float(i.split(' ')[1][0:-1]) for i in points]
        self.points = list(zip(points_x, points_y))

  
