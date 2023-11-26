let notificationCount = 0;

document.addEventListener("DOMContentLoaded", function () {
	notificationCount = 2;
	updateNotificationCount();
});

function updateNotificationCount() {
	const countElement = document.getElementById("notificationCount");
	countElement.textContent = notificationCount;
}

function toggleDropdown() {
	var dropdown = document.getElementById("notificationDropdown");
	dropdown.classList.toggle("active");
}

function sendNotification() {
	// Assuming you have a function to add a notification to the database
	// You would replace the following lines with your actual implementation
	const senderId = 1; // Replace with the actual sender's ID
	const receiverId = 2; // Replace with the actual receiver's ID
	addNotificationToDatabase(senderId, receiverId);

	// Update the notification count and UI
	notificationCount++;
	updateNotificationCount();
}
