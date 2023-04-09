import 'package:http/http.dart' show get;

class APICaller {
  static String baseUrl = "";
  static String addEndpoint = "$baseUrl/";
  static String deleteEndpoint = "$baseUrl/";
  static String updateEndpoint = "$baseUrl/";

  static addPackage({required String url}) async {
    print("added $url");
    try {
      var url = Uri.parse(baseUrl + addEndpoint);
      var response = await get(url);
      if (response.statusCode == 200) {
        // Something
      }
    } catch (e) {
      print(e);
    }
    // Must check if package with same name and version already exists or not
  }

  static deletePackages() {}

  static updatePackages() {}

  static factoryReset() {}
}
