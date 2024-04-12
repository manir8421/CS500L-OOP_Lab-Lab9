# 20099_Md_Maniruzzaman_Lab10
# CS500L(A)_SFBU
# Lab_10_Q01

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class Displayable(ABC):
    @abstractmethod
    def display():
        pass


class House(Displayable):
    def __init__(self, address, squareFeet, numRooms, price: float):
        self.__address = address
        self.__squareFeet = squareFeet
        self.__numRooms = numRooms
        self.__price = price

    # add some public properties here if necessary 

    @property
    def address(self) -> str:
        return self.__address
    
    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float):
        self.__price = new_price
    

    def __eq__(self, __value: object) -> bool:
        if  isinstance(__value, House):
            return self.__address == __value.__address
        return False
    


    def __str__(self) -> str:
        return f"Address = {self.__address}, Square Feet = {self.__squareFeet}, Num of Rooms = {self.__numRooms}, Price = {self.__price}"

    def __repr__(self) -> str:
        return str(self)
    
    def display(self):
        print(self)


class Contact(Displayable):
    def __init__(self, firstName, lastName, phoneNumber, email):
        self.__lastName = lastName
        self.__firstName = firstName
        self.__email = email
        self.__phoneNumber = phoneNumber

    # add some public properties here if necessary 
        
    @property
    def lastName(self):
        return self.__lastName
    
    @property
    def firstName(self):
        return self.__firstName
    
    @property
    def email(self):
        return self.__email
    
    @property
    def phoneNumber(self):
        return self.__phoneNumber

    def __eq__(self, __value: object) -> bool:
        if  isinstance(__value, Contact):
            return self.__email == __value.__email
        return  False

    def __str__(self) -> str:
        return f"Last Name = {self.__lastName}, First Name= {self.__firstName}, Phone Number = {self.__phoneNumber}, Email={self.__email}"
    
    def __repr__(self) -> str:
        return str(self)

    def display(self):
        print(self)


class Owner(Contact):
    def __init__(self, lastName, firstName, phoneNumber, email):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__houses = []

    def addHouse(self, house):
        self.__houses.append(house)

    def __str__(self) -> str:
        output = super().__str__() + "\n"
        output += "Owner of the following houses:\n"
        for house in self.__houses:
            output += str(house) + "\n"
        return output
    
    def display(self):
        pass


class Buyer(Contact):
    def __init__(self, lastName, firstName, phoneNumber, email):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__watchList = []

    @property
    def watchList(self):
        return self.__watchList

    #  Save the house in his watch list 
    def saveForLater(self, house):
        self.__watchList.append(house)

    # Remove the house from his watch list
    def removeFromSaveForLater(self, house):
        if house in self.__watchList:
            self.__watchList.remove(house)

    def __str__(self) -> str:
        watchListStr = '\n'.join(str(house) for house in self.__watchList)
        return (f"Last Name = {self.lastName}, First Name = {self.firstName}, "
                f"Phone Number = {self.phoneNumber}, Email = {self.email}\n"
                "Watching the following houses:\n"
                f"{watchListStr}")

    def display(self):
        print(self)


class Company(Displayable):
    def __init__(self, companyName):
        self.__companyName = companyName
        self.__owners: list[Owner] = []
        self.__buyers: list[Buyer] = []
        self.__agents: list[Agent] = []
        self.__houses: list[House] = []

    def addOwner(self, owner: Owner):
        if owner not in self.__owners:
            self.__owners.append(owner)

    def addBuyer(self, buyer: Buyer):
        if buyer not in self.__buyers:
            self.__buyers.append(buyer)

    def addAgent(self, agent: Agent):
        if agent not in self.__agents:
            self.__agents.append(agent)

    def addHouseToListing(self, house: House):
        if house not in self.__houses:
            self.__houses.append(house)

    def getHouseByAddress(self, address: str) -> Optional[House]:
        for house in self.__houses:
            if house.address == address:
                return house
        return None

    def removeHouseFromListing(self, house: House):
        if house in self.__houses:
            self.__houses.remove(house)
            self.removeHouseFromSaveForLater(house)

    def removeHouseFromSaveForLater(self, house: House):
        for buyer in self.__buyers:
            buyer.removeFromSaveForLater(house)

    def getBuyersByHouse(self, house: House) -> list[Buyer]:
        interested_buyers = [buyer for buyer in self.__buyers if house in buyer.watchList]
        return interested_buyers

    def __str__(self) -> str:
        output = f"Company Name = {self.__companyName}\n"
        output += "=========================== The list of agents ===========================\n"
        for agent in self.__agents:
            output += f"{agent}\n"
        output += "=========================== The house listing ===========================\n"
        for house in self.__houses:
            output += f"{house}\n"
        output += "=========================== The list of owners ===========================\n"
        for owner in self.__owners:
            output += f"{owner}\n"
        output += "=========================== The list of buyers ===========================\n"
        for buyer in self.__buyers:
            output += f"{buyer}\n"
        return output

    def display(self):
        print(self)


class Agent(Contact):
    def __init__(self, lastName, firstName, phoneNumber, email, position, company: Company):
        super().__init__(lastName, firstName, phoneNumber, email)
        self.__position = position
        self.__company = company

    def addHouseToListingForOwner(self, owner, house):
        self.__company.addHouseToListing(house)
        self.__company.addOwner(owner)

    def helpBuyerToSaveForLater(self, buyer: Buyer, house: House):
        buyer.saveForLater(house)
        self.__company.addBuyer(buyer)

    def editHousePrice(self, address, newPrice):
        target_house = self.__company.getHouseByAddress(address)
        if target_house is not None:
            target_house.price = newPrice
        else:
            print(f"No house found at address '{address}'.")


    def soldHouse(self, house):
        self.__company.removeHouseFromListing(house)
        self.__company.removeHouseFromSaveForLater(house)

    # print all potential buyers who are interested in buying that house
    def printPotentalBuyers(self, house):
        potential_buyers = self.__company.getBuyersByHouse(house)
        print("Potential Buyers:")
        for buyer in potential_buyers:
            print(buyer)


    def __str__(self) -> str:
        return super().__str__() + "\n" + f"Position = {self.__position}"
    
    def display(self):
        print(self)


def main():
    owner1 = Owner('Peter', 'Li', '510-111-2222', 'peter@yahoo.com')
    owner2 = Owner('Carl', 'Buck', '408-111-2222', 'carl@yahoo.com')

    house1 = House('1111 Mission Blvd', 1000, 2, 1000000)
    house2 = House('2222 Mission Blvd', 2000, 3, 1500000)
    house3 = House('3333 Mission Blvd', 3000, 4, 2000000)

    owner1.addHouse(house1)
    owner2.addHouse(house2)
    owner2.addHouse(house3)

    buyer1 = Buyer('Tom', 'Buke', '408-555-2222', 'tom@yahoo.com')
    buyer2 = Buyer('Lily', 'Go', '510-222-3333', 'lily@yahoo.com')

    company = Company('Good Future Real Estate')
    agent1 = Agent('Dave', 'Henderson', '408-777-3333',
                   'dave@yahoo.com', 'Senior Agent', company)
    company.addAgent(agent1)

    agent1.addHouseToListingForOwner(owner1, house1)
    agent1.addHouseToListingForOwner(owner2, house2)
    agent1.addHouseToListingForOwner(owner2, house3)

    agent1.helpBuyerToSaveForLater(buyer1, house1)
    agent1.helpBuyerToSaveForLater(buyer1, house2)
    agent1.helpBuyerToSaveForLater(buyer1, house3)

    agent1.helpBuyerToSaveForLater(buyer2, house2)
    agent1.helpBuyerToSaveForLater(buyer2, house3)

    agent1.editHousePrice('2222 Mission Blvd', 1200000)

    company.display()

    print('\nAfter one house was sold ..........................')
    agent1.soldHouse(house3)
    company.display()

    print('\nDisplaying potential buyers for house 1 ..........................')
    agent1.printPotentalBuyers(house1)



if __name__ == "__main__":
    main()
