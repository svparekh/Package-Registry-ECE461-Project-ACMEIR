import 'package:http/http.dart' show Response, delete, get, post, put;

class APICaller {
  // API Url
  static const String apiBaseUrl =
      "https://rgdoy0o5q0.execute-api.us-east-2.amazonaws.com/beta";
  // Internal vars (for help with variables of endpoints)
  static const String _packageByName = "$apiBaseUrl/package/byName";
  static const String _packageByID = "$apiBaseUrl/package";
  // API Endpoints
  static const String authEndpoint = "$apiBaseUrl/authenticate";
  static String packageByNameEndpoint(String name) => '$_packageByName/$name';
  static String packageByIdEndpoint(int id) => '$_packageByID/$id';
  static String packageRateByIdEndpoint(int id) => '$_packageByID/$id/rate';
  static const String addEndpoint = "$apiBaseUrl/package";
  static const String packagesEndpoint = "$apiBaseUrl/packages";
  static const String resetEndpoint = "$apiBaseUrl/reset";
  // For testing
  static String test = "https://";

  static Future<bool> addPackage({required String url}) async {
    try {
      var apiUrl = Uri.parse(test);
      var response = await post(apiUrl);
      if (response.statusCode == 200) {
        return true;
      }
    } catch (e) {
      print(e);
    }
    return false;
  }

  static Future<bool> deletePackages(
      {required List<Map<String, dynamic>> packages}) async {
    try {
      var apiUrl = Uri.parse(test);
      var response = await delete(apiUrl);
      if (response.statusCode == 200) {
        return true;
      }
    } catch (e) {
      print(e);
    }
    return false;
  }

  static Future<bool> updatePackages(
      {required List<Map<String, dynamic>> packages}) async {
    try {
      var apiUrl = Uri.parse(test);
      var response = await put(apiUrl);
      if (response.statusCode == 200) {
        return true;
      }
    } catch (e) {
      print(e);
    }
    return false;
  }

  static Future<bool> factoryReset() async {
    try {
      Uri apiUrl = Uri.parse(resetEndpoint);
      Response response = await delete(apiUrl);
      if (response.statusCode == 200) {
        print(response);
        print(response.body);
        return true;
      }
    } catch (e) {
      print(e);
    }
    return false;
  }
}
