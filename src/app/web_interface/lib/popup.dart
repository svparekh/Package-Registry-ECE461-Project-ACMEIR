import 'dart:async';
import 'dart:convert';
import 'dart:html' show FileReader, FileUploadInputElement;
import 'package:fluent_ui/fluent_ui.dart';

import 'api.dart' show APICaller;

showSuccessFailInfoBar(BuildContext context, bool success, String type) {
  if (success) {
    displayInfoBar(context, builder: (context, close) {
      return InfoBar(
        title: Text('Successful $type!'),
        content: Text(
            '${type == 'Add' ? 'Adding' : type == 'Update' ? 'Updating' : type == 'Delete' ? 'Deleting' : type} was successfuly completed.'),
        action: IconButton(
          icon: const Icon(FluentIcons.clear),
          onPressed: close,
        ),
        style: InfoBarThemeData(
          decoration: (severity) {
            return const BoxDecoration(color: Colors.white);
          },
        ),
        severity: InfoBarSeverity.success,
      );
    });
  } else {
    displayInfoBar(context, builder: (context, close) {
      return InfoBar(
        title: Text('Failed to $type!'),
        content: Text(
            '${type == 'Add' ? 'Adding' : type == 'Update' ? 'Updating' : type == 'Delete' ? 'Deleting' : type} could not be succesfuly completed. Please try again another time.'),
        action: IconButton(
          icon: const Icon(FluentIcons.clear),
          onPressed: close,
        ),
        style: InfoBarThemeData(
          decoration: (severity) {
            return const BoxDecoration(color: Colors.white);
          },
        ),
        severity: InfoBarSeverity.error,
      );
    });
  }
}

Future<bool> showPackageDialog(BuildContext context,
    {required String type, List<Map<String, dynamic>>? packages}) async {
  // Type can be of types: 'Add', 'Update', 'Delete', or 'Reset'
  // Returns false if canceled and true if main action button pressed
  final bool? result = await showDialog<bool>(
    context: context,
    builder: (context) {
      // Vars and stream setup
      final TextEditingController controllerURL = TextEditingController();
      final TextEditingController controllerCode = TextEditingController();
      String pickedFileContent = '';
      StreamController<bool> isWorkingStream =
          StreamController<bool>.broadcast();
      isWorkingStream.add(false);
      StreamController<String> pickedFileName =
          StreamController<String>.broadcast();
      final reader = FileReader();
      // Determine type
      Widget body;
      if (type == 'Add') {
        body = Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Pick a zip package or enter URL'),
            ),
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: FilledButton(
                child: StreamBuilder<String>(
                  stream: pickedFileName.stream,
                  builder: (context, snapshot) {
                    return Text(
                        (snapshot.hasData) ? snapshot.data! : 'Pick package');
                  },
                ),
                onPressed: () async {
                  FileUploadInputElement fileUploadInput =
                      FileUploadInputElement();
                  fileUploadInput.accept = '.zip';
                  fileUploadInput.click();

                  fileUploadInput.onChange.listen((e) {
                    final files = fileUploadInput.files;
                    if (files != null && files.length == 1) {
                      final file = files[0];

                      reader.onLoadStart.listen((event) {
                        pickedFileName.add('Loading package...');
                      });

                      reader.onLoad.listen((e) {
                        final bytes = reader.result as List<int>;
                        pickedFileContent = base64Encode(bytes);
                        // pickedFileContent = reader.result.toString().substring(
                        //     41); // remove 'data:application/x-zip-compressed;base64,'
                        pickedFileName.add(file.name);
                      });
                      reader.readAsArrayBuffer(file);

                      // Convert the file contents to a base64 encoded string

                      // reader.readAsDataUrl(file);
                    }
                  });
                  // FilePickerResult? result = await FilePicker.platform
                  //     .pickFiles(
                  //         allowedExtensions: ['zip'],
                  //         type: FileType.custom,
                  //         allowMultiple: false,
                  //         lockParentWindow: true,
                  //         dialogTitle: 'Pick a zip package to upload');

                  // if (result != null) {
                  //   pickedFileContent = base64Encode(
                  //       File(result.files.single.path!).readAsBytesSync());
                  // } else {
                  //   // User canceled the picker
                  // }
                },
              ),
            ),
            TextBox(
              placeholder: 'Enter npm URL',
              controller: controllerURL,
            ),
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('JS Program:'),
            ),
            TextBox(
              placeholder: 'Program',
              minLines: 3,
              maxLines: 6,
              controller: controllerCode,
            ),
          ],
        );
      } else if (type == 'Update') {
        body = packages == null
            ? Container()
            : Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '${packages.length == 1 ? 'Package' : 'Packages'} listed below will be updated if available.',
                    style: const TextStyle(fontSize: 16),
                  ),
                  for (Map<String, dynamic> pack in packages)
                    Text(
                        pack['Name']) // CHECK IF A PACKAGE CAN BE UDPATED FIRST
                ],
              );
      } else if (type == 'Delete') {
        body = packages == null
            ? Container()
            : Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'If you delete ${packages.length == 1 ? 'this package' : 'these packages'}, you won\'t be able to recover ${packages.length == 1 ? 'it' : 'them'}. Do you want to delete ${packages.length == 1 ? 'it' : 'them'}?',
                    style: const TextStyle(fontSize: 16),
                  ),
                  for (Map<String, dynamic> pack in packages) Text(pack['Name'])
                ],
              );
      } else if (type == 'Reset') {
        body = Text(
          'Are you sure you want to reset the app to default state?',
          style: const TextStyle(fontSize: 16),
        );
      } else {
        body = const Text('Invalid dialog type');
      }
      // Dialog
      return ContentDialog(
        title: Text('$type package'),
        content: StreamBuilder<bool>(
            stream: isWorkingStream.stream,
            builder: (context, snapshot) {
              return (snapshot.hasData && snapshot.data == true)
                  ? const SizedBox(
                      height: 32, width: double.infinity, child: ProgressBar())
                  : body;
            }),
        actions: [
          StreamBuilder<bool>(
              stream: isWorkingStream.stream,
              builder: (context, snapshot) {
                return FilledButton(
                  onPressed: (snapshot.hasData && snapshot.data == true)
                      ? null
                      : () async {
                          isWorkingStream.add(true);

                          if (type == 'Add') {
                            await APICaller.addPackage(
                                    data: controllerURL.text.isEmpty
                                        ? pickedFileContent
                                        : controllerURL.text,
                                    code: controllerCode.text)
                                .then((value) {
                              showSuccessFailInfoBar(context, value, type);
                              Navigator.pop(context, value);
                            });
                          }
                          // else if (type == 'Update') {
                          //   await APICaller.updatePackages(packages: packages!)
                          //       .then((value) {
                          //     showSuccessFailInfoBar(context, value, type);
                          //     Navigator.pop(context, value);
                          //   });
                          // }
                          else if (type == 'Delete') {
                            await APICaller.deletePackages(packages: packages!)
                                .then((value) {
                              showSuccessFailInfoBar(context, value, type);
                              Navigator.pop(context, value);
                            });
                          } else if (type == 'Reset') {
                            await APICaller.factoryReset().then((value) {
                              showSuccessFailInfoBar(context, value, type);
                              Navigator.pop(context, value);
                            });
                          }
                        },
                  child: Text(type),
                );
              }),
          StreamBuilder<bool>(
              stream: isWorkingStream.stream,
              builder: (context, snapshot) {
                return Button(
                  onPressed: (snapshot.hasData && snapshot.data == true)
                      ? null
                      : () {
                          reader.abort();
                          Navigator.pop(context, false);
                        },
                  child: const Text('Cancel'),
                );
              }),
        ],
      );
    },
  );
  return result ?? false;
}

Future<String> showPropertiesDialog(BuildContext context,
    {required Map<String, dynamic> data}) async {
  final int size = await APICaller.packageSize(package: data);
  final result = await showDialog<String>(
      context: context,
      builder: (context) => ContentDialog(
            style: const ContentDialogThemeData(
                bodyStyle: TextStyle(fontSize: 20)),
            title: const Text('Properties'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  propertyRow(name: 'Name', value: data['Name'].toString()),
                  propertyRow(name: 'ID', value: data['ID'].toString()),
                  propertyRow(
                      name: 'Rating',
                      value: double.parse('${data['NetScore']}')
                          .toStringAsFixed(2)),
                  propertyRow(
                      name: 'Version', value: data['Version'].toString()),
                  propertyRow(name: 'Size', value: '$size bytes'),
                ],
              ),
            ),
            actions: [
              FilledButton(
                child: const Text('Close'),
                onPressed: () => Navigator.pop(context, 'canceled'),
              ),
            ],
          ));
  return result ?? 'canceled';
}

Widget propertyRow({required String name, required String value}) {
  return Container(
    decoration: BoxDecoration(
        color: const Color.fromARGB(255, 235, 235, 235),
        borderRadius: BorderRadius.circular(7)),
    padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
    margin: const EdgeInsets.all(5),
    child: Column(
      children: [
        Padding(
          padding: EdgeInsets.only(bottom: (value.length > 20) ? 7 : 0),
          child: Row(
            children: [
              Text(
                style: const TextStyle(fontWeight: FontWeight.bold),
                name,
                textAlign: TextAlign.start,
              ),
              const Spacer(),
              Text(
                value.length > 20 ? '' : value,
                textAlign: TextAlign.end,
              )
            ],
          ),
        ),
        if (value.length > 20)
          SingleChildScrollView(
            child: Text(
              style: TextStyle(
                fontSize: 14,
              ),
              value,
            ),
          )
      ],
    ),
  );
}
