using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class SpawnManager : MonoBehaviour
{
    public CarAgent[] agentsPrefabs;
    public TrafficLightAgent trafficLightPrefab;
    public MoveController moveControllerPrefab;
    SimulationInfo simulationInfo;
    public Transform pivot;

    public void SpawnAgents(SimulationInfo simulationInfo)
    {
        this.simulationInfo = simulationInfo;
        foreach (var agent in simulationInfo.agents)
        {
            AgentComponent agentComponent = null;
            switch (agent.type)
            {
                case 0:// Vehicle
                    BuildCar(ref agentComponent, agent);
                    break;
                case 1:// Traffic Light
                    BuildTrafficLight(ref agentComponent, agent);
                    break;
                default:
                    break;
            }
            agentComponent.agentId = agent.agentId;
            agentComponent.type = agent.type;
        }
    }

    void BuildCar(ref AgentComponent agentComponent, Agent agent)
    {
        int randomInt = UnityEngine.Random.Range(0, agentsPrefabs.Length);
        agentComponent = Instantiate(agentsPrefabs[randomInt], pivot, false);
        agentComponent.name = agentsPrefabs[randomInt].name + " ID: " + agent.agentId;
        MoveController moveController = Instantiate(moveControllerPrefab, pivot, false);
        moveController.name = "Move Controller ID " + agent.agentId;
        agentComponent.GetComponent<CarAgent>().target = moveController.transform;
        moveController.steps = GetSteps(agent.agentId);
        Vector3 position = new Vector3(moveController.steps[0].StepInfo.positionX, 0, moveController.steps[0].StepInfo.positionY);
        agentComponent.transform.localPosition = position;
        moveController.enabled = true;
    }

    void BuildTrafficLight(ref AgentComponent agentComponent, Agent agent)
    {
        agentComponent = Instantiate(trafficLightPrefab, pivot, false);
        agentComponent.name = "Traffic Light ID: " + agent.agentId;
        var steps = GetSteps(agent.agentId);
        Vector3 position = new Vector3(steps[0].StepInfo.positionX, 0, steps[0].StepInfo.positionY);
        agentComponent.transform.localPosition = position;
        agentComponent.GetComponent<TrafficLightAgent>().steps = steps;
    }

    Step[] GetSteps(int id)
    {
        var steps = from step in simulationInfo.steps
                    where step.StepInfo.agentId == id
                    select step;
        return steps.ToArray();
    }
}
