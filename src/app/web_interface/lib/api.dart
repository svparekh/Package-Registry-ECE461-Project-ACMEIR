import 'package:http/http.dart' show get, delete, post, put;

class APICaller {
  // API Url
  static const String apiBaseUrl =
      "https://rgdoy0o5q0.execute-api.us-east-2.amazonaws.com/beta";
  // Internal vars (for help with variables of endpoints)
  static const String _packageByName = "$apiBaseUrl/package/byName";
  static const String _packageByID = "$apiBaseUrl/package";
  // API Endpoints
  static const String authEndpoint = "$apiBaseUrl/authenticate";
  static const String addEndpoint = "$apiBaseUrl/package";
  static const String packagesEndpoint = "$apiBaseUrl/packages";
  static const String resetEndpoint = "$apiBaseUrl/reset";
  static String packageByNameEndpoint(String name) => '$_packageByName/$name';
  static String packageByIdEndpoint(int id) => '$_packageByID/$id';
  static String packageRateByIdEndpoint(int id) => '$_packageByID/$id/rate';
  // For testing
  static String test = "/";

  static Future<bool> addPackage({required String url}) async {
    try {
      Uri apiUrl = Uri.parse(test);
      var response = await post(apiUrl);
      if (response.statusCode == 200) {
        // Something
        return true;
      }
    } catch (e) {
      print(e);
    }
    return false;
  }

  static Future<bool> deletePackages(
      {required List<Map<String, dynamic>> packages}) async {
    bool isComplete = true;
    for (Map<String, dynamic> package in packages) {
      try {
        Uri apiUrl = Uri.parse(packageByIdEndpoint(package['id']));
        var response = await delete(Uri.parse(test));
        if (response.statusCode == 200) {
          // Something
        }
      } catch (e) {
        print(e);
        isComplete = false;
      }
    }
    return isComplete;
  }

  static Future<bool> updatePackages(
      {required List<Map<String, dynamic>> packages}) async {
    bool isComplete = true;
    for (Map<String, dynamic> package in packages) {
      try {
        Uri apiUrl = Uri.parse(packageByIdEndpoint(package['id']));
        var response = await put(Uri.parse(test));
        if (response.statusCode == 200) {
          // Something
        }
      } catch (e) {
        print(e);
        isComplete = false;
      }
    }
    return isComplete;
  }

  static Future<bool> factoryReset() async {
    try {
      Uri apiUrl = Uri.parse(resetEndpoint);
      var response = await delete(apiUrl);
      if (response.statusCode == 200) {
        print(response);
        print(response.body);
        // Something
        return true;
      }
    } on Error catch (e) {
      print(e);
    }
    return false;
  }
}
