import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { CCDIKSolver } from "three/examples/jsm/animation/CCDIKSolver.js";
let headBone;
let thighL;
let shinL;
let thigh_original_rotation;
let shin_original_rotation;
let upperArmBoneL, forearmBoneL, handBoneL, target_handL, original_positionL; // Left hand bones
let upperArmBoneR, forearmBoneR, handBoneR, target_handR, original_positionR; // Right hand bones
let model;
let solverL, solverR; // Separate solvers for each hand
let skeleton;
let target_handL_axis;
let skinnedMesh;
let base_bone;
function add_rigged_model(scene) {
    const loader = new GLTFLoader();
    loader.load("test_ik4.glb", function (gltf) {
        model = gltf.scene;
        model.traverse((node) => {
            console.log(node.name);
            node.traverse((child) => {
                if (child.type === "SkinnedMesh") {
                    skinnedMesh = child;
                }
            });
        }
        );
        let bonesNotFound = ["thighL", "shinL", "head", "upper_armL", "forearmL", "handL", "index_target_handL", "upper_armR", "forearmR", "handR", "index_target_handR", "spine" ];
        if (skinnedMesh) {
            skinnedMesh.skeleton.bones.forEach((bone) => {
                switch (bone.name) {
                    case "thighL":
                        console.log("Found thighL bone");
                        thighL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "thighL");
                        break;
                    case "shinL":
                        console.log("Found shinL bone");
                        shinL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "shinL");
                        break;
                    case "head":
                        console.log("Found head bone");
                        headBone = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "head");
                        break;
                    case "upper_armL":
                        console.log("Found upper_armL bone");
                        upperArmBoneL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "upper_armL");
                        break;
                    case "forearmL":
                        console.log("Found forearmL bone");
                        forearmBoneL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "forearmL");
                        break;
                    case "handL":
                        console.log("Found handL bone");
                        handBoneL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "handL");
                        break;
                    case "index_target_handL":
                        console.log("Found index_target_handL bone");
                        target_handL = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "index_target_handL");
                        break;
                    case "upper_armR":
                        console.log("Found upper_armR bone");
                        upperArmBoneR = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "upper_armR");
                        break;
                    case "forearmR":
                        console.log("Found forearmR bone");
                        forearmBoneR = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "forearmR");
                        break;
                    case "handR":
                        console.log("Found handR bone");
                        handBoneR = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "handR");
                        break;
                    case "index_target_handR":
                        console.log("Found index_target_handR bone");
                        target_handR = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "index_target_handR");
                        break;
                    case "spine":
                        console.log("Found spine bone");
                        base_bone = bone;
                        bonesNotFound = bonesNotFound.filter((item) => item !== "spine");
                        break;
                }

            });
            if (bonesNotFound.length > 0) {
                console.error("Some bones not found: ", bonesNotFound);
            }
            //lets add a axis helper on the target_handL
            target_handL_axis = new THREE.AxesHelper(1);

            scene.add(target_handL_axis);
            thigh_original_rotation = thighL.rotation.clone();
            shin_original_rotation = shinL.rotation.clone();
            setupIKSolver(skinnedMesh, true); // Setup left hand IK Solver
            setupIKSolver(skinnedMesh, false); // Setup right hand IK Solver

            skeleton = new THREE.SkeletonHelper(model);
            skeleton.visible = true;
            scene.add(skeleton);
            // let helper = solverL.createHelper(0.01);
            // let helper2 = solverR.createHelper(0.01);
            // helper.scale.set(0.1, 0.1, 0.1);
            // scene.add(helper);
            // scene.add(helper2);
            scene.add(model);
            original_positionL = target_handL.position.clone();
            original_positionR = target_handR.position.clone();
        } else {
            console.error("SkinnedMesh not found.");
        }
    });
}

let leftIK, rightIK;

function setupIKSolver(skinnedMesh, isLeft) {
    const side = isLeft ? 'L' : 'R';
    const upperArmBone = isLeft ? upperArmBoneL : upperArmBoneR;
    const forearmBone = isLeft ? forearmBoneL : forearmBoneR;
    const handBone = isLeft ? handBoneL : handBoneR;
    const target_hand = isLeft ? target_handL : target_handR;
    const solver = isLeft ? solverL : solverR;

    const index_upperArm = skinnedMesh.skeleton.bones.indexOf(upperArmBone);
    const index_forearm = skinnedMesh.skeleton.bones.indexOf(forearmBone);
    const index_hand = skinnedMesh.skeleton.bones.indexOf(handBone);
    const index_target_hand = skinnedMesh.skeleton.bones.indexOf(target_hand);
    //check if all bones are found
    if (index_upperArm === -1 || index_forearm === -1 || index_hand === -1 || index_target_hand === -1) {
        console.error("Bone not found.");
        return;
    }
    

    if (isLeft) {
        leftIK = [{
            target: index_target_hand,
            effector: index_hand,
            links: [
                {
                    index: index_forearm, rotationMin: new THREE.Vector3(0, 0, 0 ),rotationMax: new THREE.Vector3( 2, - .3, .3 )
                },
                {
                    index: index_upperArm,
                },
            ]
        }];
        solverL = new CCDIKSolver(skinnedMesh, leftIK);
    } else {
        rightIK = [{
            target: index_target_hand,
            effector: index_hand,
            links: [
                {
                    index: index_forearm, rotationMin: new THREE.Vector3(0, 0, 0 ),rotationMax: new THREE.Vector3( 2, .3, .3 )
                },
                {
                    index: index_upperArm
                },
            ]
        }];
        solverR = new CCDIKSolver(skinnedMesh, rightIK);
    }
}

let currentIteration = 0;
let currentLink = 0;
let step = 0;
let maxSteps = 100;
function incrementalTestLimits() {
    //check rigkIK limits
    let links = rightIK[0].links;
    let link = links[currentLink];
    let bone = skinnedMesh.skeleton.bones[link.index];
    // bone.rotation.x = link.rotationMax.x;
    let span_max_to_min = link.rotationMax.x - link.rotationMin.x;
    let step_size = span_max_to_min / maxSteps;
    let current_value = link.rotationMin.x + step_size * step;
    bone.rotation.x = current_value;
    if (step === maxSteps) {
        step = 0;
    }
    step += 1;
}

// function incrementalTestLimits() {
//     //check rigkIK limits
//     let links = rightIK[0].links;
//     let link = links[currentLink];
//     let bone = skinnedMesh.skeleton.bones[link.index];
//     // bone.rotation.x = link.rotationMax.x;
//     let span_max_to_min = link.rotationMax.y - link.rotationMin.y;
//     let step_size = span_max_to_min / maxSteps;
//     let current_value = link.rotationMin.y + step_size * step;
//     bone.rotation.y = current_value;
//     if (step === maxSteps) {
//         step = 0;
//     }
//     step += 1;
// }


let solver_enabled = true;
let show_joint_limits = false;
function animateModel(positionL, positionR, headRotation, thighquat) {
    if (solver_enabled) {
        solverL.update();
        solverR.update();
    }
    if (show_joint_limits) {
        incrementalTestLimits();
    }
    target_handL.position.copy(positionL);
    target_handR.position.copy(positionR);
    headBone.rotation.set(headRotation.x, headRotation.y, headRotation.z);
    thighL.quaternion.copy(thighquat);
    // //get world rotation of the thigh bone
    let worldRotation = new THREE.Quaternion();
    thighL.getWorldQuaternion(worldRotation);
    let euler = new THREE.Euler();
    euler.setFromQuaternion(worldRotation);
    // shinL.rotation.x = (shinRotation.x -euler.x + Math.PI);
    shinL.rotation.x = (shin_original_rotation.x - euler.x + Math.PI);
}




export { add_rigged_model, animateModel };
