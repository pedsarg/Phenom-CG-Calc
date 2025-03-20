import json
import math
import time
import matplotlib.pyplot as plt
import os
from pdfEditor import generatePDF

def getFuelValue(fuelWeight):
    try:
        with open('storage/fuel.json', 'r') as file:
            data = json.load(file)

        fuel_str = str(fuelWeight)

        if fuel_str in data:
            return data[fuel_str]
        else:
            fuelWeight -= 10
            return getFuelValue(fuelWeight)
        
    except FileNotFoundError:
        print("File not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return None


def getFuelArm(fuelWeight):
    fuelWeightAdjusted = (math.floor(fuelWeight / 10) * 10)
    fuelArm = getFuelValue(fuelWeightAdjusted)
    return fuelArm


def getUserInput():
    userInput = {}
    
    print("- Balance Data:")
    userInput["crewWeight"] = float(input("\nCrew weight: "))
    userInput["sideFacingSeatWeight"] = float(input("\nSide facing seat weight: "))
    userInput["passengers1And2Weight"] = float(input("\nPassengers 1 and 2 weight: "))
    userInput["passengers3And4Weight"] = float(input("\nPassengers 3 and 4 weight: "))
    userInput["beltedToiletSeatWeight"] = float(input("\nBelted toilet seat weight: "))
    userInput["forwardBaggageCompartmentWeight"] = float(input("\nForward baggage compartment weight: "))
    userInput["lhAftCabinetWeight"] = float(input("\nLH Aft cabinet weight: "))
    userInput["aftBaggageCompartmentWeight"] = float(input("\nAft baggage compartment weight: ")) 
    userInput["takeOffFuelWeight"] = float(input("\nTake off fuel weight: "))
    userInput["landingFuelWeight"] = float(input("\nLanding fuel weight: "))

    return userInput
    

def getDefualtValues():
    try:
        with open('storage/defaultValues.json','r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return None


def getValuesFromData(data, key):
    try:
        if key in data:
            return data[key]
        else:
            raise Exception("Error getting default values")
    except Exception as e:
        print(f"Exception: {e}")
        return 0


def getArmValues():
    data = getDefualtValues()
    return getValuesFromData(data, "armValues")


def getWeightValues():
    data = getDefualtValues()
    return getValuesFromData(data, "weightValues")


def calculateMoment(userInformation, weight, arm):
    return {
        'basicEmptyMoment' : (arm['basicEmptyArm'] * weight['basicEmptyWeight']),
        'crewMoment' : (arm['crewArm'] * userInformation['crewWeight']),
        'sideFacingSeatMoment' : (arm['sideFacingSeatArm'] * userInformation['sideFacingSeatWeight']),
        'passengers1And2Moment' : (arm['passengers1And2Arm'] * userInformation['passengers1And2Weight']),
        'passengers3And4Moment' : (arm['passengers3And4Arm'] * userInformation['passengers3And4Weight']),
        'beltedToiletSeatMoment' : (arm['beltedToiletSeatArm'] * userInformation['beltedToiletSeatWeight']),
        'forwardBaggageCompartmentMoment' : (arm['forwardBaggageCompartmentArm'] * userInformation['forwardBaggageCompartmentWeight']),
        'lhAftCabinetMoment' : (arm['lhAftCabinetArm'] * userInformation['lhAftCabinetWeight']),
        'aftBaggageCompartmentMoment' : (arm['aftBaggageCompartmentArm'] * userInformation['aftBaggageCompartmentWeight'])
    }


def calculateAdjustedZeroFuel(userInformation, weights, moments):
    weight = (weights['basicEmptyWeight'] + userInformation['crewWeight'] + userInformation['sideFacingSeatWeight'] + userInformation['passengers1And2Weight'] + userInformation['passengers3And4Weight'] + userInformation['beltedToiletSeatWeight'] + userInformation['forwardBaggageCompartmentWeight'] + userInformation['lhAftCabinetWeight'] + userInformation['aftBaggageCompartmentWeight'])
    moment = (moments['basicEmptyMoment'] + moments['crewMoment'] + moments['sideFacingSeatMoment'] + moments['passengers1And2Moment'] + moments['passengers3And4Moment'] + moments['beltedToiletSeatMoment'] + moments['forwardBaggageCompartmentMoment'] + moments['lhAftCabinetMoment'] + moments['aftBaggageCompartmentMoment'])
    arm = moment / weight
    return {
        'weight' : weight,
        'moment' : moment,
        'arm' : arm
    }


def caculateTakeoffFuelMoment(fuelWeight, fuelArm):
    return (fuelWeight * fuelArm)


def calculateCGAndWeight(adjustedZeroFuel, fuelWeight, FuelMoment):
    weight = adjustedZeroFuel['weight'] + fuelWeight
    moment = adjustedZeroFuel['moment'] + FuelMoment
    arm = moment / weight
    return {
        'weight': weight,
        'moment': moment,
        'arm': arm
    }


def calculateCG(arm):
    return (((arm - 5.325) / 1.64) * 100)


def graphParameters():
    data = getDefualtValues()
    return getValuesFromData(data, "graphLimits")


def graphGenerator(graphInformation):
    graphLimits = graphParameters()

    fig, ax = plt.subplots(figsize=(6, 8))

    ax.plot(graphLimits['limitCG'], graphLimits['limitWeight'], 'k-')
    ax.plot(graphLimits['lineAboveCG'], graphLimits['lineAboveWeight'], 'k-')
    ax.plot(graphLimits['sideLineCG'], graphLimits['sideLineWeight'], 'k--')

    ax.scatter(graphInformation['takeOffCG'], graphInformation['AirplaneCGAndWeightTakeoff'][1], color='red', zorder=3, label="Take Off")
    ax.scatter(graphInformation['landingCG'], graphInformation['AirplaneCGAndWeightLanding'][1], color='blue', zorder=3, label="Landing")

    ax.set_xlabel("CG POSITION - %MAC")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("CG Position")
    ax.legend()

    ax.grid(True, linestyle="--", alpha=0.6)

    plt.savefig("graph.png", dpi=300, bbox_inches='tight')


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def cgCalculator():
    clearTerminal()
    userInformation = getUserInput()
    weights = getWeightValues()
    arms = getArmValues()
    moments = calculateMoment(userInformation, weights, arms)
    adjustedZeroFuel = calculateAdjustedZeroFuel(userInformation, weights, moments)
    
    takeOfFuelArm = getFuelArm(userInformation['takeOffFuelWeight'])
    takeOffFuelMoment = caculateTakeoffFuelMoment(takeOfFuelArm, userInformation['takeOffFuelWeight'])
    cgAndWeightTakeoff = calculateCGAndWeight(adjustedZeroFuel, userInformation['takeOffFuelWeight'], takeOffFuelMoment)
    takeOffCG = calculateCG(cgAndWeightTakeoff['arm'])

    landingFuelArm = getFuelArm(userInformation['landingFuelWeight'])
    landingFuelMoment = (landingFuelArm * userInformation['landingFuelWeight'])
    cgAndWeightLanding = calculateCGAndWeight(adjustedZeroFuel, userInformation['landingFuelWeight'], landingFuelMoment)
    landingCG = calculateCG(cgAndWeightLanding['arm'])
    
    tableValues = {
        'bew': [arms['basicEmptyArm'], weights['basicEmptyWeight'], moments['basicEmptyMoment']],
        'crew': [arms['crewArm'], userInformation['crewWeight'], moments['crewMoment']],
        'sideFacingSeat': [arms['sideFacingSeatArm'], userInformation['sideFacingSeatWeight'], moments['sideFacingSeatMoment']],
        'passengers1And2': [arms['passengers1And2Arm'], userInformation['passengers1And2Weight'], moments['passengers1And2Moment']],
        'passengers3And4': [arms['passengers3And4Arm'], userInformation['passengers3And4Weight'], moments['passengers3And4Moment']],
        'beltedToiletSeat': [arms['beltedToiletSeatArm'], userInformation['beltedToiletSeatWeight'], moments['beltedToiletSeatMoment']],
        'forwardBaggageCompartment': [arms['forwardBaggageCompartmentArm'], userInformation['forwardBaggageCompartmentWeight'], moments['forwardBaggageCompartmentMoment']],
        'lhAftCabinet': [arms['lhAftCabinetArm'], userInformation['lhAftCabinetWeight'], moments['lhAftCabinetMoment']],
        'aftBaggageCompartment': [arms['aftBaggageCompartmentArm'], userInformation['aftBaggageCompartmentWeight'], moments['aftBaggageCompartmentMoment']],
        'maximumZeroFuel': [adjustedZeroFuel['weight']],
        'adjustedZeroFuel': [adjustedZeroFuel['arm'], adjustedZeroFuel['weight'], adjustedZeroFuel['moment']],
        'takeOffFuel': [takeOfFuelArm, userInformation['takeOffFuelWeight'], takeOffFuelMoment],
        'landingFuel': [landingFuelArm, userInformation['landingFuelWeight'], landingFuelMoment],
        'AirplaneCGAndWeightTakeoff': [cgAndWeightTakeoff['arm'], cgAndWeightTakeoff['weight'], cgAndWeightTakeoff['moment']],
        'takeOffCG': [takeOffCG],
        'AirplaneCGAndWeightLanding': [cgAndWeightLanding['arm'], cgAndWeightLanding['weight'], cgAndWeightLanding['moment']],
        'landingCG': [landingCG],
    }

    graphGenerator(tableValues)
    return tableValues


def getFlightInformation():
    flightData = {}

    print(" - Flight Data:")
    flightData["LogBookPage"] = input("\n    Enter the Log Book Page:")
    flightData["dateFlight"] = input("\n    Enter the date of the flight:")
    flightData["prefix"] = input("\n    Enter the aircraft prefix:")
    flightData["model"] = input("\n    Enter the aircraft model:")
    flightData["operator"] = input("\n    Enter the operator:")
    flightData["cityOrigin"] = input("\n    Enter the city of origin:")
    flightData["ICAOOrigin"] = input("\n    Enter the ICAO code of origin:")
    flightData["cityDestination"] = input("\n    Enter the city of destination:")
    flightData["ICAODestination"] = input("\n    Enter the ICAO code of destination:")
    flightData["takeOffHour"] = input("\n    Enter the take off hour:")
    flightData["landingHour"] = input("\n    Enter the landing hour:")
    flightData["pilot"] = input("\n    Enter the pilot:")
    flightData["pilotLicense"] = input("\n    Enter the pilot license:")
    flightData["copilot"] = input("\n    Enter the copilot:")
    flightData["copilotLicense"] = input("\n    Enter the copilot license:")

    return flightData


def getPassengersData():
    passengersList = []

    print("\n - Passengers:")
    while 1:
        numberOfPassengersStr = input("\n    Enter the number of passengers:")

        if numberOfPassengersStr == "":
            break;
        else:
            numberOfPassengers = int(numberOfPassengersStr)

            if numberOfPassengers<=6:
                for i in range(numberOfPassengers):
                    name = input(f"\n    Enter the name of passenger {i + 1}:")
                    document = input(f"\n    Enter the document of passenger {i + 1}:")
                    passengerData = {'name': name, 'document': document}
                    passengersList.append(passengerData)
                break
            else:
                print("\n 6 passengers is the maximum capacity!")
        
    return passengersList


def checkNotesLength(notes):
    while 1:
        if len(notes) <= 262:
            return notes
        else:
            clearTerminal()
            print("\n Maximum characters limit (280) reached!")
            notes = input("\n Enter the note again: ")


def getNotesData():        
    print("\n - Notes:")
    notes = {}
    
    note = input("\n    Enter the Atis: ")
    notes["atis"] = checkNotesLength(note)
    note = ""

    note = input("\n    Enter the RTO: ")
    notes["rto"] = checkNotesLength(note)
    note = ""

    note = input("\n    Enter the clearance: ")
    notes["clearance"] = checkNotesLength(note)
    note = ""

    return notes


def getFlightReportData():
    clearTerminal()
    flightData = {}

    flightInformation = getFlightInformation();
    flightData["flightInformation"] = flightInformation
    clearTerminal()
    passengersData = getPassengersData()
    flightData["passengers"] = passengersData
    clearTerminal()
    tableValues = cgCalculator()
    flightData["tableValues"] = tableValues
    clearTerminal()
    notesData = getNotesData()
    flightData["notes"] = notesData

    return flightData


def generateFlightReport():
    flightData = getFlightReportData()
    
    try:
        output_pdf_path = generatePDF(flightData)
    except ValueError as e:
        print("{e}");
    
    clearTerminal()
    print(f" Flight Report created successfully: {output_pdf_path}")
    input("\nPress enter to continue!")


def changeDefaultValues():
    clearTerminal()

    print("Enter the new values for the following fields\n  if you want to keep the default value, just press enter")
    armValues = getArmValues()
    weightValues = getWeightValues()
    graphLimits = graphParameters()

    print("\nArm values")
    for key in armValues:
        newValue = input(f"{key} ({armValues[key]}): ")
        if newValue != "":
            armValues[key] = float(newValue)
    
    print("\n\nWeight values")
    for key in weightValues:
        newValue = input(f"{key} ({weightValues[key]}): ")
        if newValue != "":
            weightValues[key] = float(newValue)
    
    print("\n\nGraph values")
    for key in graphLimits:
        newValue = input(f"{key} ({graphLimits[key]}): ")
        if newValue != "":
            graphLimits[key] = list(map(float, newValue.split()))
    
    changedValues = {
        'armValues': armValues,
        'weightValues': weightValues,
        'graphLimits': graphLimits
    }

    with open("storage/defaultValues.json", "w") as file:
        json.dump(changedValues, file)
    
    clearTerminal()
    print("Values changed successfully!")
    time.sleep(3)


def main():
    while 1:
        clearTerminal()
        print("\n 1 - Calculate CG\n 2 - Generate flight report\n 3 - Change the default values\n 4 - Exit")
        option = int(input("Enter an option:")) 

        match option:
            case 1:
                clearTerminal()
                print("Calculating CG...")
                time.sleep(3)
                cgAndWeightData = cgCalculator()
                print(f"Take Off CG: {cgAndWeightData['takeOffCG'][0]:.2f} \nTake Off Weight: {cgAndWeightData['AirplaneCGAndWeightTakeoff'][1]}") 
                print(f"\nLanding CG: {cgAndWeightData['landingCG'][0]:.2f} \nLanding Weight: {cgAndWeightData['AirplaneCGAndWeightLanding'][1]}")
                input("\nPress enter to continue!")
            case 2:
                clearTerminal()
                print("Generate flight report!")
                generateFlightReport()
                time.sleep(3)
            case 3:
                clearTerminal()
                print("Change the default values!")
                time.sleep(3)
                changeDefaultValues()
            case 4:
                clearTerminal()
                print("Exiting...")
                time.sleep(3)
                return 0
            case _:
                clearTerminal()
                time.sleep(3)
                print("Invalid option")


if __name__ == "__main__": 
    main()