import { writable } from 'svelte/store';
import { onMount } from 'svelte';


function createLimbsDataStore() {
  // Try to read the stored value from local storage
  const stored = localStorage.getItem('limb');


  const initialValue = stored ? JSON.parse(stored) : [
    {
      "name": "Chest",
      "rotationX": 0,
      "rotationY": -16,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": 0,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "1",
      "connected": false,
      "connectedTo": "none"
    },
    {
      "name": "Upper Arm Right",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.375,
      "positionY": 0.3125,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "8",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Forearm Right",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -1,
      "positionY": -1,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "9",
      "connected": true,
      "connectedTo": "Upper Arm Right"
    },
    {
      "name": "Upper Arm Left",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.25,
      "positionY": 0.3125,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "6",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Forearm Left",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 1,
      "positionY": -1,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "7",
      "connected": true,
      "connectedTo": "Upper Arm Left"
    },
    {
      "name": "Head",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": 0.3999999999999999,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "head",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Waist",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": -0.3999999999999999,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "head",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Right Leg",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.125,
      "positionY": -0.5,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "2",
      "connected": true,
      "connectedTo": "Waist"
    },
    {
      "name": "Left Leg",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.125,
      "positionY": -0.5,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "3",
      "connected": true,
      "connectedTo": "Waist"
    },
    {
      "name": "Right Foot",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.125,
      "positionY": -0.9375,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "4",
      "connected": true,
      "connectedTo": "Right Leg"
    },
    {
      "name": "Left Foot",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.125,
      "positionY": -0.9375,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "5",
      "connected": true,
      "connectedTo": "Left Leg"
    }
  ]


  // Create a writable store with the initial value
  const { subscribe, set, update } = writable(initialValue);

  return {
    subscribe,
    set: (value) => {
      localStorage.setItem('limb', JSON.stringify(value)); // Save to local storage
      set(value); // Update the store's value
    },
    update
  };
}


export function resetLocalStorage() {
  localStorage.removeItem('limb');
  const default_val = [
    {
      "name": "Chest",
      "rotationX": 0,
      "rotationY": -16,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": -0.3999999999999999,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "1",
      "connected": false,
      "connectedTo": "none"
    },
    {
      "name": "Upper Arm Right",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.375,
      "positionY": 0.3125,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "8",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Forearm Right",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -1,
      "positionY": -1,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "9",
      "connected": true,
      "connectedTo": "Upper Arm Right"
    },
    {
      "name": "Upper Arm Left",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.25,
      "positionY": 0.3125,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "6",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Forearm Left",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 1,
      "positionY": -1,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "7",
      "connected": true,
      "connectedTo": "Upper Arm Left"
    },
    {
      "name": "Head",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": 0.3999999999999999,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "head",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Waist",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0,
      "positionY": -0.3999999999999999,
      "positionZ": 0,
      "send": false,
      "vrchat_name": "head",
      "connected": true,
      "connectedTo": "Chest"
    },
    {
      "name": "Right Leg",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.125,
      "positionY": -0.5,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "2",
      "connected": true,
      "connectedTo": "Waist"
    },
    {
      "name": "Left Leg",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.125,
      "positionY": -0.5,
      "positionZ": 0,
      "send": true,
      "vrchat_name": "3",
      "connected": true,
      "connectedTo": "Waist"
    },
    {
      "name": "Right Foot",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": 0.125,
      "positionY": -0.9375,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "4",
      "connected": true,
      "connectedTo": "Right Leg"
    },
    {
      "name": "Left Foot",
      "rotationX": 0,
      "rotationY": 0,
      "rotationZ": 0,
      "positionX": -0.125,
      "positionY": -0.9375,
      "positionZ": 0.0625,
      "send": true,
      "vrchat_name": "5",
      "connected": true,
      "connectedTo": "Left Leg"
    }
  ]



  limbs_data.set(default_val);
}
export const limbs_data = createLimbsDataStore();



