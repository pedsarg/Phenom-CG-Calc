import json
import math
import matplotlib.pyplot as plt

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


def initializeArmValues():
    return {
        'basicEmptyArm' : 5.990,
        'crewArm' : 2.952,
        'sideFacingSeatArm' : 3.622,
        'passengers1And2Arm' : 4.336,
        'passengers3And4Arm' : 5.612,
        'beltedToiletSeatArm' : 6.344,
        'forwardBaggageCompartmentArm' : 1.155,
        'lhAftCabinetArm' : 6.344,
        'aftBaggageCompartmentArm' : 7.983
    }


def initializeWeightValues():
    return {
        'basicEmptyWeight' : 3211,
        'maximumZeroFuelWeight' : 3830,
    }


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


def graphGenerator(graphInformation):
    limitWeight = [3000, 3220, 4030, 4750, 4750, 4030, 3420, 3000]
    limitCG = [35.0, 21.5, 21.5, 23.5, 36.9, 38.5, 38.5, 35.0]

    lineAboveWeight = [4430, 4430]
    lineAboveCG = [22.7 , 37.6]

    sideLineWeight = [3220, 3220, 4030, 4750, 4750]
    sideLineCG = [21.5, 19.5, 19.5, 21.5, 23.5]

    fig, ax = plt.subplots(figsize=(6, 8))

    ax.plot(limitCG, limitWeight, 'k-')
    ax.plot(lineAboveCG, lineAboveWeight, 'k-')
    ax.plot(sideLineCG, sideLineWeight, 'k--')

    ax.scatter(graphInformation['takeOffCG'], graphInformation['takeOffWeight'], color='red', zorder=3, label="Take Off")
    ax.scatter(graphInformation['landingCG'], graphInformation['landingWeight'], color='blue', zorder=3, label="Landing")

    ax.set_xlabel("CG POSITION - %MAC")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("CG Position")
    ax.legend()

    ax.grid(True, linestyle="--", alpha=0.6)

    plt.savefig("graph.png", dpi=300, bbox_inches='tight')



def main():
    userInformation = getUserInput()
    weights = initializeWeightValues()
    arms = initializeArmValues()
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
    
    graphInformation = {
        'takeOffCG': takeOffCG,
        'takeOffWeight': cgAndWeightTakeoff['weight'],
        'landingCG': landingCG,
        'landingWeight': cgAndWeightLanding['weight']
    }

    graphGenerator(graphInformation)

    print(f"CG: {takeOffCG:.3f} \nWeight: {cgAndWeightTakeoff['weight']:.3f}") 
    print(f"\nLanding CG: {landingCG:.3f} \nLanding Weight: {cgAndWeightLanding['weight']:.3f}")


if __name__ == "__main__": 
    main()