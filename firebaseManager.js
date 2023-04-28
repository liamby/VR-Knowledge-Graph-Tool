// Import the Firebase SDK
import firebase from "firebase/app";
import "firebase/database";

// Initialize Firebase with your project's config
const firebaseConfig = {
    apiKey: "AIzaSyA4MyejiXQ4qfXAoQ1GCpbyUeGIhohLRcQ",
    authDomain: "vr-knowledge-graph.firebaseapp.com",
    databaseURL: "https://vr-knowledge-graph-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "vr-knowledge-graph",
    storageBucket: "vr-knowledge-graph.appspot.com",
    messagingSenderId: "1040556725785",
    appId: "1:1040556725785:web:fe1eee51937e3365ea7c88",
    measurementId: "G-4HMB94DK00"
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the Firebase Realtime Database
const database = firebase.database();

// Retrieves the JSON child object stored at "child" key of the Firebase Realtime Database
function getJsonFromRealtimeDatabase(child) {
    return database.ref(child).once("value").then(snapshot => {
        return snapshot.val();
    });
}

// Updates the JSON child object stored at "child" key of the Firebase Realtime Database
function updateJsonFromRealtimeDatabase(child, newJson) {
    return database.ref(child).set(newJson);
}

// Export the functions as a module
export { getJsonFromRealtimeDatabase, updateJsonFromRealtimeDatabase };