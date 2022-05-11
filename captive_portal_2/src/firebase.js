import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
const firebaseConfig = {
    apiKey: "AIzaSyDsR4MN62Ej3wIS5606SJEJsAsd5J1CTRQ",
    authDomain: "users-informations-391bc.firebaseapp.com",
    projectId: "users-informations-391bc",
    storageBucket: "users-informations-391bc.appspot.com",
    messagingSenderId: "198348211710",
    appId: "1:198348211710:web:be052bdbebae02bb252caf",
    measurementId: "G-XJR2W2RLJ8"
  };
  export const app = initializeApp(firebaseConfig)
  export const storage = getStorage(app)