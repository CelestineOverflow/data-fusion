<script>
    import Explosion from './Explosion.svelte';
	import HowItWork from './HowItWork.svelte';
</script>

<div id="container">
	<Explosion />
	<div id="text">
		<h1>Data Fusion</h1>
		<section>
            <h1>About the Project</h1>
            <p>
                Our project integrates inexpensive Inertial Measurement Units (IMUs) with AprilTag detection to develop a robust motion tracking and motion capture system tailored for gaming and virtual reality experiences. This innovative solution significantly reduces the cost and complexity typically associated with real-time motion tracking technologies.
            </p>
            <h2>Objective</h2>
            <p>
                The primary objective is to create an affordable  yet effective motion capture system that leverages the strengths of both IMU sensors and AprilTag visual markers. By combining these technologies, we aim to provide near-perfect motion tracking accuracy, essential for immersive VR experiences and advanced gaming setups.
            </p>
            <h2>Technology Overview</h2>
            <p>
                IMUs provide rapid motion data by measuring linear and angular motion with accelerometers and gyroscopes. However, IMUs alone can suffer from drift over time. To counteract this, we integrate AprilTag recognition, which offers high-precision positional data whenever the tags are within the camera's field of view.
            </p>
            <p>
                By using AprilTags to periodically recalibrate the IMU data, our system can correct any drift errors dynamically, maintaining accurate tracking throughout usage. This setup is particularly advantageous in environments where camera-based data may not be continuously available due to line-of-sight issues or other constraints.
            </p>
            <h2>Application and Benefits</h2>
            <p>
                This dual-system approach not only enhances the reliability and accuracy of motion tracking in VR and gaming but also offers it at a fraction of the cost of traditional motion capture systems. It's an ideal solution for developers seeking to implement motion capture in their projects without the substantial investment typically required.
            </p>
            <h2>Technical Challenges and Solutions</h2>
            <p>
                One of the main challenges involves the integration of real-time data from both the IMUs and AprilTags. While IMUs provide quick updates, processing AprilTag data can be relatively slower using OpenCV. To address this, our system prioritizes IMU data for continuous motion tracking, using AprilTag data for periodic adjustments and accuracy enhancements.
            </p>
            <h2>Github Repository</h2>
            <p>
                For more information and access to our project code, please visit our GitHub repository at <a href="https://github.com/CelestineOverflow/data-fusion"> github.com/CelestineOverflow/data-fusion</a>
            </p>
        </section>
	</div>
</div>
<div id="container">
	
	<div id="text">
		<h1>How It Works?</h1>
		<section>
            <h1>About the Project</h1>
            <p>
                Our project integrates inexpensive Inertial Measurement Units (IMUs) with AprilTag detection to develop a robust motion tracking and motion capture system tailored for gaming and virtual reality experiences. This innovative solution significantly reduces the cost and complexity typically associated with real-time motion tracking technologies.
            </p>
        </section>
	</div>
    <HowItWork />
</div>
<div id="container">
	<img class="img" src="Screenshot.png" alt="IMU AprilTag Fusion System Diagram" />
    
    <img class="img" src="IRL_Board.jpeg" alt="IRL Board" />
<div id="text">
    <h1>How is it made</h1>
    <section>
        <h1>About the Project</h1>
        <p>
            To create your own version of the Data Fusion sensor, you can follow the following link to the project's OSHW-Lab project page <a href="https://oshwlab.com/celestine.s.machuca/motion-fusion"> here</a>
        </p>
    </section>
</div>

</div>
<style>
	#container {
		display: flex; /* Establishes a flex container */
		align-items: center; /* Vertically align items in the middle */
		justify-content: space-around; /* Distributes space around items */
		height: 100vh; /* Optional: takes full viewport height */
	}

	#text {
		flex: 1; /* Allows the text block to grow and shrink */
		padding: 20px; /* Adds some spacing around the text */
	}
    .img {
    width: 20%;  /* Sets the width to 50% of its container */
    height: auto;  /* Sets the height to auto, preserving the aspect ratio */
    flex: 1;  /* Allows the image block to grow and shrink */
    padding: 20px;  /* Adds some spacing around the image */
}
</style>
