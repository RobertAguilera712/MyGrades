document.addEventListener("DOMContentLoaded", function (event) {
	const showNavbar = (toggleId, navId, bodyId, headerId) => {
		const toggle = document.getElementById(toggleId),
			nav = document.getElementById(navId),
			bodypd = document.getElementById(bodyId),
			headerpd = document.getElementById(headerId);

		// Validate that all variables exist
		if (toggle && nav && bodypd && headerpd) {
			toggle.addEventListener("click", () => {
				// show navbar
				nav.classList.toggle("showDashboard");
				// change icon
				toggle.classList.toggle("bi-x-lg");
				toggle.classList.toggle("bi-list");
				// add padding to body
				bodypd.classList.toggle("body-pd");
				// add padding to header
				headerpd.classList.toggle("body-pd");
			});
		}
	};

	showNavbar("header-toggle", "nav-bar", "body-pd", "header");

	/*===== LINK ACTIVE =====*/
	const linkColor = document.querySelectorAll(".nav_link");

	function colorLink() {
		if (linkColor) {
			linkColor.forEach((l) => l.classList.remove("active"));
			this.classList.add("active");
		}
	}
	linkColor.forEach((l) => l.addEventListener("click", colorLink));

	// Your code to run since DOM is loaded and ready
});


function addImageFilesListeners() {

	document.querySelector('input[type=file].image')?.addEventListener('change', (e) => {
		const reader = new FileReader();
		reader.onload = () => {
			const previewImg = e.target.parentElement.querySelector('img.preview');
			previewImg.setAttribute('src', reader.result);
		}
		reader.readAsDataURL(e.target.files[0]);
	});

	document.querySelectorAll('input[type=file].document').forEach(node => {
		node.addEventListener("change", (e) => {
			const files = e.target.files;
			const fileName = files[0].name;
			console.log("file name: ", fileName);
			const fileLabel = e.target.parentElement.querySelector("label.file-name")
			fileLabel.textContent = fileName;
		});
	})
}


function disableValidation() {
	document.querySelectorAll(".no-validate").forEach((i) => {
		i.addEventListener("click", (e) => {
			document.querySelector("form").noValidate = true;
		});
	});
}


document.addEventListener("DOMContentLoaded", function () {
	disableValidation();
	addImageFilesListeners();
});

document.body.addEventListener('htmx:afterSwap', function () {
	// Check if the swap target is your table or container
	disableValidation();
	addImageFilesListeners();
});