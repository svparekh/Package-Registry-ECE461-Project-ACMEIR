class APICaller {
  static String baseUrl = "";
  static String endpoint = "$baseUrl/";

  static addPackage({required String url}) {
    print("added $url");
    // Must check if package with same name and version already exists or not
  }

  static deletePackages() {}

  static updatePackages() {}

  static factoryReset() {}
}
