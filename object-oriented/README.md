## OOP
- code gets bigger and complicated (like code for delivery drone).
- we can solve by breaking the functionality into several objects so that different people can work on different things and can combine.
- And also we can use previously built functionality in to different projects(like buliding camera app) 
- So,OOP is paradigm, a way to think about our code,a way for us to structure our code so that if code gets bigger and bigger we can able to be organized.

### Class and objects:
Basic class and object

    class BigObject:   #Class
      #code
      pass

    obj1= BigObject    #instantiate
    
 - Class is like a blueprint from which objects can be instantiated.
 - The class is going to be stored in memory so python interpreter is going to say to check that same memory when an object is instantiated.
 
### Creating Our Own Objects

    class PlayCharacter:
        membership=True # Class object attribute which doesn't change across objects
        def __init__(self,name='anonymus'):   #__init__ is called dunder or magic menthod . This is also constructor for class.
            if(PlayerCharacter.membership):   # you can access Class_object_attributes directly without self unlike normal attributes(self.name)
                self.name=name    #attributes

        def run(self):
            print('run')

        @classmethod              
        def add_things(cls,num1,num2):  #Difference from above method is,we can use this function without instantiating class as mentioned below print statement.
            return(num1,num2)

        @staticmethod
        def add_things2(num1,num2): #we dont care ablut class-state when using static methods
            return(num1+num2)
    player1=PlayerCharacter('Cindy')
    print(player1)
    print(player1.name)
    player2=PlayerCharacter('Tom')
    player2.attack=50
    print(player2.name)
    print(player2.run())
    print(player2.attack)

    help(player1) # will give entire blueprint(code of class) of the object 
    help(list) #similarly this will give entire blueprint of python datatype

    #print(player1.add_things(2,3))
    print(PlayerCharacter.add_things(2,3))

    ouput:
    <__main__.PlayerCharacter object ar 0x7fc55028ecb8>
    Cindy
    Tom  
    run  # by executing run() function
    None  # the result returned by 'run' function
    50
    5  #class method

- above(___init__) method is called constrcutor class.
- above 'self' refers to player character.
- above 'name' is attribute which you can access them by dot
- attributes('name')  are unique to the object
- ClassObject_attribute('membership') which doesn't change across objects


## Four pillars of OOP
### Encapsulation:
- encapsulation is binding of data and functions (that manipulate the data).we encapsulate into one big object so that we keep wnerything in box .
- example is above mentioned.
### Abstraction:
- abstraction means hiding of information or abstracting away information and giving access to neccessary things.
- Examples are all built-in-functions of python. There are abstracted from us and we just use the methods instaed of coding from scrach
#### Public and private variables:
- In python there is no true private variables unlike java
- If we want to create a method or attribute private we just keep underscore before it as convention but still it is just for our understnding of private variables only.

        class PlayerCharacter:
            def __init__(self,name,age):
                self._name=name
                self._age=age

### Inhertance:
- we can inherit classes in child classes by passing parent-class.
- For example if you have a game in which  different kind of users present like 'Wizard','Archer' but all kind of users need to login.so in this case we will pass User parent class into child-classes


        class User():
            def sign_in(self):
                print('logged in')

        class Wizard(User):
            pass

        class Archer(User):
            pass


        wizard1=Wizard()
        print(wizard1.sign_in())
        print(isinstance(wizard1,Wizard)) #isinstance checks whether object is instance of class
        print(isinstance(wizard1,User))  #Gives true because Wizard class inheruts User class
        print(isinstance(wizard1,object)) # Gives true because python inherits from base 'object' class

        output:
        logged in
        None #response of no-return statement from function
        True
        True
        True


### Polymorphism:

The idea of polymorphism refers to the way in which object classes can share same method name but those method names can act differently based on what object call it.

        class User():
            def sign_in(self):
                print('logged in')
            def attck(self):
                print('do nothing')

        class Wizard(User):
            def __init__(self,name,power):
                self.name=name
                self.power=power
            def attack(self):
                User.attck(self)
                print(f'attcking with {self.power}')

        class Archer(User):
            pass


        wizard1=Wizard('abc',60)
        print(wizard1.attack())

        output:
        do nothing
        attcking with 60 
        None  #response of no-return statement from function



### super()
What if we want to use common attributes in the parent-class(from where we inherit) instead of children class . To solve this , we can initiate parent-class using normal-convention or using super() method

        class User():
            def __init__(self,email):
                self.email=email
            def sign_in(self):
                print('logged in')

        class Wizard(User):
            def __init__(self,name,power,email):   #since this is the only constructer that runs when object is initiated we need to set all attribute values at here only
                #User.__init__(self,email) #This is one way
                super().__init__(email)  #This is second way
                self.name=name
                self.power=power
            def attack(self):
                User.attck(self)
                print(f'attcking with {self.power}')


        wizard1=Wizard('abc',60,'prudhvi@gmail.com'))
        print(wizard1.email)
        dir(wizard1) #if you printed this will print all the methods available for this wizard object
        
        output:
        prudhvi@gmail.com

### Object introspection

using dir() we can get the all methods available for the object .Refer above example


### Dunder methods:
https://docs.python.org/3/reference/datamodel.html#special-method-names
#By reading the python documentation, add 3 more magic/dunder methods of your choice to this Toy class. 

        class Toy():
          def __init__(self, color, age):
            self.color = color
            self.age = age
            self.my_dict = {
                'name':'Yoyo',
                'has_pets': False,
            }

          def __str__(self):
            return f"{self.color}"

          def __len__(self):
            return 5

          def __del__(self):
            return "deleted"

          def __call__(self):
              return('yes??')

          def __getitem__(self,i):
              return self.my_dict[i]


        action_figure = Toy('red', 0)
        print(action_figure.__str__())
        print(str(action_figure))
        print(len(action_figure))
        print(action_figure())
        print(action_figure['name'])

        ouput:
        red
        red
        5
        yes??
        Yoyo
        
        
        
        class SuperList(list):
          def __len__(self):
            return 1000

        super_list1 = SuperList();

        print(len(super_list1))
        super_list1.append(5)
        print(super_list1[0])
        print(issubclass(list, object))

        output:
        1000
        5
        True


### MRO(method resolution order)
Used depth first search and gives correct order of execution when in case of multiple-complex inheritances.
https://repl.it/@aneagoie/MRO
http://www.srikanthtechnologies.com/blog/python/mro.aspx


### Decorators:
Decorators are having '@' sign before them
Example:
@classmethod
@staticmethd

- Functions are like just variables in python

        def hello():
            print("hellooo")

        greet=hello
        del helo   # what it does is i am going to delete name reference to this function(hello()) present in memory but it wont delete the function as greet is pointing to it above

        print(greet())

        output:
        hellooo
        None
        
  
 #### Higher Order Function:
- Higher order function are the functions which accept another function as parameter or returns a function.Example are map,reduce becasue they are accepting functions

#### Decorator:
A decorator supercharges a function. It is simply a function that wraps another function and enhances it.

basic-Example:

    def my_decorator(func):   #taking input as function
        def wrap_func():      #warpping it(function)
            print("**********")
            func()
            print("**********")
        return wrap_func      #returning wrapped function

    @my_decorator
    #behind the scenes this means 
    '''
    hello2=my_decorator(hello)
    hello2()
    '''
    #or simply as
    '''
    my_decorator(hello)()
    '''
    def hello():
        print("hello")
    hello()

    output:
    **********
    hello
**********

#### Decorator pattern:
using below pattern,we can pass 'n' number of parameters when caling a function(here it is hello())

    def my_decorator(func):   #taking input as function
        def wrap_func(*args,**kwargs):      #warpping it(function)
            print("**********")
            func(*args,**kwargs)
            print("**********")
        return wrap_func      #returning wrapped function

    @my_decorator
    def hello(greeting,emoji=':|'):  #here emoji is keyword argument and greeting is argument
        print(greeting,emoji)
        
    hello('hii')
    
    output:
    **********
    hello  :|
    **********

Example:

    #performance decorator.
    from time import time
    def performance(fn):
      def wrapper(*args, **kwargs):
        t1 = time()
        result = fn(*args, **kwargs)
        t2 = time()
        print(f'took {t2-t1}')
        return result
      return wrapper

    @performance
    def long_time():
        for i in range(10000):
            i*5

    long_time()
    
    output:
    took 0.0006716251373291016
    
    
### Generators:
Generator allows us to use speciall keyword 'yield' so that it can stop and resume functions
Example:
- Generator generate one at a time without taking memory

        for i in range(10)  # we are giving value one at a time to 'i' and we are not storing in our memory using range-generaator
        for i in [1,2,3,4,5,6,7,8,9,10] # here unlike above we are storing
        
- Generator is subset of iterables.

- Behind the hood range()  uses generators like as below using yield

        def geerator_function(num):
            for i in range(n):
                yield i*2

        g= geerator_function(1)  #creates a generator object
        next(g)  #output here is 0*2=0
        next(g)  #output here is 1*2=2
        
 example:
 
        ###########
        from time import time
        def performance(fn):
            def wrapper(*args, **kawrgs):
                t1 = time()
                result = fn(*args, **kawrgs)
                t2 = time()
                print(f'took {t2-t1} s')
                return result
            return wrapper

        @performance
        def long_time():
            print('1')
            for i in range(100000):
                i*5
        @performance
        def long_time2():
            print('2')
            for i in list(range(100000)):
                i*5


        long_time()
        long_time2()

        outout:
        1
        took 0.02527761459350586 s
        2
        took 0.010668754577636719 s

#### Under the hood of generators:

    def special_for(iterable):
      iterator = iter(iterable)
      while True:
        try:
          iterator*5
          next(iterator)
        except StopIteration:
          break


    class MyGen:
      current = 0
      def __init__(self, first, last):
        self.first = first
        self.last = last
        MyGen.current = self.first #this line allows us to use the current number as the starting point for the iteration

      def __iter__(self):
        return self

      def __next__(self):
        if MyGen.current < self.last:
          num = MyGen.current
          MyGen.current += 1
          return num
        raise StopIteration

    gen = MyGen(1,100)
    for i in gen:
        print(i)
