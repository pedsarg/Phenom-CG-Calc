import json
import math
import time
import matplotlib.pyplot as plt
import os

def getFuelValue(fuelWeight):
    try:
        with open('fuel.json', 'r') as file:
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
    return {
        'crewWeight' : 150,
        'sideFacingSeatWeight' : 75,
        'passengers1And2Weight' : 150,
        'passengers3And4Weight' : 150,
        'beltedToiletSeatWeight' : 1,
        'forwardBaggageCompartmentWeight' : 1,
        'lhAftCabinetWeight' : 1,
        'aftBaggageCompartmentWeight' : 30, 
        'takeOffFuelWeight' : 715,
        'landingFuelWeight' : 160
    }


def getDefualtValues():
        try:
            with open('defaultValues.json','r') as file:
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

    ax.scatter(graphInformation['takeOffCG'], graphInformation['takeOffWeight'], color='red', zorder=3, label="Take Off")
    ax.scatter(graphInformation['landingCG'], graphInformation['landingWeight'], color='blue', zorder=3, label="Landing")

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
    
    cgAndWeghtData = {
        'takeOffCG': takeOffCG,
        'takeOffWeight': cgAndWeightTakeoff['weight'],
        'landingCG': landingCG,
        'landingWeight': cgAndWeightLanding['weight']
    }

    graphGenerator(cgAndWeghtData)
    
    return cgAndWeghtData


def getFlightReportData():
    clearTerminal()
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

    print("\n - Passengers:")
    numberOfPassengers = int(input("\n    Enter the number of passengers:"))
    passengersList = []
    for i in range(numberOfPassengers):
        name = input(f"\n    Enter the name of passenger {i + 1}:")
        document = input(f"\n    Enter the document of passenger {i + 1}:")
        passengerData = {'name': name, 'document': document}
        passengersList.append(passengerData)
    flightData["passengers"] = passengersList

    print("\n - Notes:")
    flightData["atis"] = input("\n    Enter the Atis:")
    flightData["rto"] = input("\n    Enter the RTO:")
    flightData["clearance"] = input("\n    Enter the clearance:")

    return flightData


def generateFlightReport():
    cgAndWeightData = cgCalculator()
    flightData = getFlightReportData()

    print("\n - Flight Data:")

    for key in flightData:
        if key == "passengers":
            print("\n - Passengers:")
            for passenger in flightData[key]:
                print(f"    Name: {passenger['name']} - Document: {passenger['document']}")
        else:
            if key == "atis":
                print("\n - Notes:")
            print(f"    {key}: {flightData[key]}")
    
    print("\n - CG and Weight Data:")

    for key in cgAndWeightData:
        print(f"    {key}: {float(cgAndWeightData[key]):.3f}")

    input("\nPress enter to continue")


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

    with open("defaultValues.json", "w") as file:
        json.dump(changedValues, file)
    
    print("Values changed successfully")
    time.sleep(3)


def main():

    while 1:
        clearTerminal()
        print("\n 1 - Calculate CG\n 2 - Generate flight report\n 3 - Change default values\n 4 - Exit")
        option = int(input("Enter an option:")) 

        match option:
            case 1:
                clearTerminal()
                print("Calculating CG...")
                time.sleep(3)
                cgAndWeightData = cgCalculator()
                print(f"CG: {cgAndWeightData['takeOffCG']:.3f} \nWeight: {cgAndWeightData['takeOffWeight']:.3f}") 
                print(f"\nLanding CG: {cgAndWeightData['landingCG']:.3f} \nLanding Weight: {cgAndWeightData['landingWeight']:.3f}")
                input("\nPress enter to continue")
            case 2:
                clearTerminal()
                print("Flight report generated")
                generateFlightReport()
                time.sleep(3)
            case 3:
                clearTerminal()
                print("Default values changed")
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