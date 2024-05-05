import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { CCDIKSolver } from "three/examples/jsm/animation/CCDIKSolver.js";

let upperArmBoneL, forearmBoneL, handBoneL, target_handL;
let upperArmBoneR, forearmBoneR, handBoneR, target_handR; // Right hand bones
let model;
let solverL, solverR; // Separate solvers for each hand
let skeleton;

function add_rigged_model(scene) {
    const loader = new GLTFLoader();
    loader.load("test_ik3.glb", function (gltf) {
        model = gltf.scene;
        let skinnedMesh;
        model.traverse((node) => {
            if (node.name === "lowman_shoes") {
                node.traverse((child) => {
                    if (child.type === "SkinnedMesh") {
                        skinnedMesh = child;
                    }
                });
            }
        });

        if (skinnedMesh) {
            skinnedMesh.skeleton.bones.forEach((bone) => {
                switch (bone.name) {
                    case "upper_armL": upperArmBoneL = bone; break;
                    case "forearmL": forearmBoneL = bone; break;
                    case "handL": handBoneL = bone; break;
                    case "index_target_handL": target_handL = bone; break;
                    case "upper_armR": upperArmBoneR = bone; break; // Identifying right hand bones
                    case "forearmR": forearmBoneR = bone; break;
                    case "handR": handBoneR = bone; break;
                    case "index_target_handR": target_handR = bone; break;
                }
            });

            setupIKSolver(skinnedMesh, true); // Setup left hand IK Solver
            setupIKSolver(skinnedMesh, false); // Setup right hand IK Solver

            skeleton = new THREE.SkeletonHelper(model);
            skeleton.visible = true;
            scene.add(skeleton);
            scene.add(model);
        } else {
            console.error("SkinnedMesh not found.");
        }
    });
}

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

    const iks = [{
        target: index_target_hand,
        effector: index_hand,
        links: [
            {
                index: index_forearm,
                rotationMin: new THREE.Vector3(1.2, -1.8, -0.4),
                rotationMax: new THREE.Vector3(1.7, -1.1, 0.3),
            },
            {
                index: index_upperArm,
            },
        ]
    }];

    if (isLeft) {
        solverL = new CCDIKSolver(skinnedMesh, iks);
    } else {
        solverR = new CCDIKSolver(skinnedMesh, iks);
    }
}

function animateModel(positionL, positionR) {
    solverL.update();
    solverR.update();
    target_handL.position.copy(positionL);
    target_handR.position.copy(positionR);
}

export { add_rigged_model, animateModel };
