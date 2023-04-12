import 'package:http/http.dart' show delete, get, post, put;

class APICaller {
  static const String apiBaseUrl =
      "https://rgdoy0o5q0.execute-api.us-east-2.amazonaws.com/beta";

  static const String authEndpoint = "$apiBaseUrl/authenticate";
  static const String _packageByName = "$apiBaseUrl/package/byName";
  static const String _packageByID = "$apiBaseUrl/package";
  static String packageByName(String name) => '$_packageByName/$name';
  static String packageByID(int id) => '$_packageByID/$id';
  static String packageByIdRate(int id) => '$_packageByID/$id/rate';
  static const String add = "$apiBaseUrl/package";
  static const String packages = "$apiBaseUrl/packages";
  static const String reset = "$apiBaseUrl/reset";

  static const String postMethod = '#post';
  static const String deleteMethod = '#delete';
  static const String getMethod = '#get';
  static const String putMethod = '#put';

  /*
  
  /
    /authenticate
    /package
      /add
      /modify
        /id
        /{id}
      /delete
        /id
          /{id}
      /get
        /name
          /{name}
        /id
          /{id}
        /rate
          /{id}
    /packages
    /reset
      

  */

  // Example for adding a package
  // baseUrl + packageByID + '/$packageID' + postMethod + addUrl

  // is there a method to make sure no two same ids appear?
  // when adding a package, they enter a url, then it goes through correctness checker, then it gets added to registry

  /* 
  Database:
  /packages
    /id
      info
      name
      version
      id
      rating
      url
  /permissions
    /user-UID
      admin
      modify
      read
      write
  */

  static String addEndpoint = "/";
  static String deleteEndpoint = "/";
  static String updateEndpoint = "/";
  static String resetEndpoint = "/";

  static Future<bool> addPackage({required String url}) async {
    try {
      var apiUrl = Uri.parse(addEndpoint);
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
      var apiUrl = Uri.parse(deleteEndpoint);
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
      var apiUrl = Uri.parse(updateEndpoint);
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
      var apiUrl = Uri.parse(reset);
      var response = await delete(apiUrl);
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
