import 'package:http/http.dart' show get;

class APICaller {
  static String baseUrl = "";
  static String addEndpoint = "$baseUrl/";
  static String deleteEndpoint = "$baseUrl/";
  static String updateEndpoint = "$baseUrl/";
  static String resetEndpoint = "$baseUrl/";

  static addPackage({required String url}) async {
    try {
      var apiUrl = Uri.parse(baseUrl + addEndpoint);
      var response = await get(apiUrl);
      if (response.statusCode == 200) {
        // Something
      }
    } catch (e) {
      print(e);
    }
    // Must check if package with same name and version already exists or not
  }

  static deletePackages() async {
    try {
      var apiUrl = Uri.parse(baseUrl + deleteEndpoint);
      var response = await get(apiUrl);
      if (response.statusCode == 200) {
        // Something
      }
    } catch (e) {
      print(e);
    }
  }

  static updatePackages() async {
    try {
      var apiUrl = Uri.parse(baseUrl + updateEndpoint);
      var response = await get(apiUrl);
      if (response.statusCode == 200) {
        // Something
      }
    } catch (e) {
      print(e);
    }
  }

  static factoryReset() async {
    try {
      var apiUrl = Uri.parse(baseUrl + resetEndpoint);
      var response = await get(apiUrl);
      if (response.statusCode == 200) {
        // Something
      }
    } catch (e) {
      print(e);
    }
  }
}
