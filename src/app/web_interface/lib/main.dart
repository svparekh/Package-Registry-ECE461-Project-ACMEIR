import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'data.dart' show PackageRegistry;
import 'firebase_options.dart' show DefaultFirebaseOptions;
import 'home.dart' show HomePage;
import 'login.dart' show LoginPage;

//
// Constants

class PresetValues {
  static const double trailingSize = 80.0;
  static const String siteName = 'ACME Package Registry';
  static const Color offwhite = Color.fromARGB(255, 241, 241, 241);
  static const Color offwhiteDark = Color.fromARGB(255, 222, 222, 222);
  static const List<String> columns = [
    "ID",
    "Package Name",
    "Version",
    "Rating",
    "Actions"
  ];
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // setup firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const WebApp());
}

class WebApp extends StatefulWidget {
  const WebApp({super.key});

  @override
  State<WebApp> createState() => _WebAppState();
}

class _WebAppState extends State<WebApp> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Future<void> didChangeAppLifecycleState(AppLifecycleState state) async {
    super.didChangeAppLifecycleState(state);
    if (state == AppLifecycleState.detached) {
      FirebaseAuth.instance.signOut();
    }
  }

  @override
  Widget build(BuildContext context) {
    return FluentApp(
      debugShowCheckedModeBanner: false,
      title: PresetValues.siteName,
      theme: FluentThemeData(brightness: Brightness.light),
      home: const NavPage(title: PresetValues.siteName),
    );
  }
}

class NavPage extends StatefulWidget {
  const NavPage({super.key, required this.title});

  // Widget for the main page containing the navbar and all other pages within it

  // Title to go on top bar
  final String title;

  @override
  State<NavPage> createState() => _NavPageState();
}

class _NavPageState extends State<NavPage> {
  // Index of current page
  int _pageIndex = 0;
  final GlobalKey _viewKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    return NavigationView(
      transitionBuilder: (child, animation) {
        return HorizontalSlidePageTransition(
            animation: animation, child: child);
      },
      key: _viewKey,
      appBar: const NavigationAppBar(
        automaticallyImplyLeading: false,
        title: Text(PresetValues.siteName, style: TextStyle(fontSize: 18)),
      ),
      pane: NavigationPane(
          selected: _pageIndex,
          items: [
            // Home page navbar item
            PaneItem(
                icon: const Icon(FluentIcons.home),
                title: const Text(
                  "Home",
                ),
                body: FutureBuilder(
                  builder: (context, snapshot) {
                    return HomePage(importDataSuccess: snapshot.data ?? false);
                  },
                  future: PackageRegistry().importData(),
                )),
            // Login navbar item
            // PaneItem(
            //     icon: const Icon(FluentIcons.contact),
            //     title: const Text(
            //       "Login",
            //     ),
            //     body: const LoginPage()),
          ],
          onChanged: (value) {
            setState(() {
              _pageIndex = value;
            });
          },
          displayMode: PaneDisplayMode.minimal),
    );
  }
}
