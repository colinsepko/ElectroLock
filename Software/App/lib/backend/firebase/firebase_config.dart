import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: const FirebaseOptions(
            apiKey: "AIzaSyAP-ORwlkGQLfwsB0KRUkgIgUMyYOOxQZg",
            authDomain: "raspui2541551.firebaseapp.com",
            projectId: "raspui2541551",
            storageBucket: "raspui2541551.firebasestorage.app",
            messagingSenderId: "1073654630063",
            appId: "1:1073654630063:web:e11392e1445bb79190b65a",
            measurementId: "G-6ZSCM6HJD1"));
  } else {
    await Firebase.initializeApp();
  }
}
