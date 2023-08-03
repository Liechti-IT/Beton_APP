# Profometer Heatmap App

![Profometer Heatmap App](screenshot.png)

Die Profometer Heatmap App ist eine Anwendung, die entwickelt wurde, um Heatmaps der Betonüberdeckung von Eisen in Stahlbeton darzustellen. Heatmaps sind eine leistungsstarke visuelle Methode, um große Mengen von Profometer-Daten zu analysieren und Muster in der Betonüberdeckung auf einen Blick zu erkennen.

## Hintergrund

Der Profometer ist ein Messgerät, das in der Bauindustrie häufig verwendet wird, um die Betonüberdeckung von Bewehrungsstäben in Stahlbetonstrukturen zu messen. Die Betonüberdeckung ist ein entscheidender Parameter für die Tragfähigkeit und Langlebigkeit von Betonkonstruktionen. Ein ausreichender Betonüberdeckungsschutz ist wichtig, um die Bewehrung vor Korrosion und anderen Umwelteinflüssen zu schützen.

Die Profometer Heatmap App bietet eine benutzerfreundliche Möglichkeit, die Rohdaten des Profometers zu visualisieren und wertvolle Einblicke in die Betonüberdeckung zu gewinnen. Die App ermöglicht es den Benutzern, verschiedene Einstellungen anzupassen, um die Heatmap an ihre spezifischen Anforderungen anzupassen.

## Funktionen

- **Datenimport**: Die App ermöglicht es Benutzern, ihre Profometer-Daten im CSV-Format hochzuladen. CSV-Daten können leicht aus den meisten Profometer-Geräten exportiert werden, wodurch die Integration mit der App nahtlos ist.

- **Benutzerdefinierte Einstellungen**: Die Benutzer können verschiedene Parameter wählen, wie die Zeichenkodierung, das Trennzeichen und das Dezimaltrennzeichen. Dadurch wird sichergestellt, dass die App mit den unterschiedlichsten Profometer-Datensätzen kompatibel ist.

- **Interpolation leerer Felder**: In manchen Fällen können Profometer-Daten Lücken oder fehlende Werte enthalten. Die App bietet eine Option, um leere Felder zu interpolieren und so eine kontinuierliche Heatmap-Darstellung zu erhalten.

- **Anpassbare Farbskala**: Benutzer können aus einer vordefinierten Auswahl an Farbskalen wählen oder ihre benutzerdefinierte Farbskala definieren. Dies ermöglicht es, die Betonüberdeckung in verschiedenen Nuancen zu visualisieren und spezifische Aspekte der Daten hervorzuheben.

- **Heatmap generieren und herunterladen**: Nachdem die Benutzer ihre Einstellungen ausgewählt und die Daten hochgeladen haben, erzeugt die App eine detaillierte Heatmap. Die Benutzer haben die Möglichkeit, die generierte Heatmap als PNG-Datei herunterzuladen, um sie für Präsentationen oder Berichte zu verwenden.

## Systemanforderungen

Um die Profometer Heatmap App auszuführen, müssen Sie die folgenden Komponenten auf Ihrem System installiert haben:

- Python 3.x: Die App ist in Python geschrieben und erfordert eine aktuelle Python-Version.

- Flask: Flask ist ein Python-Webframework, das für das Erstellen der Webanwendung verwendet wird.

- Pandas, Matplotlib, Seaborn: Diese Python-Bibliotheken sind für die Datenverarbeitung und die Erstellung der Heatmap-Grafiken notwendig.

## Installation und Ausführung

1. Stellen Sie sicher, dass Python 3.x auf Ihrem System installiert ist. Sie können es von der offiziellen Python-Website herunterladen und installieren.

2. Installieren Sie die erforderlichen Python-Pakete mit folgendem Befehl: `pip install flask pandas matplotlib seaborn`

3. Laden Sie den Quellcode der Profometer Heatmap App herunter und extrahieren Sie ihn.

4. Navigieren Sie im Terminal zur App-Verzeichnis und führen Sie den folgenden Befehl aus, um die App zu starten: `python app.py`

5. Öffnen Sie einen Webbrowser und navigieren Sie zu `http://localhost:5000/`, um auf die App zuzugreifen.

## Anleitung zur Verwendung

1. Laden Sie Ihre Profometer-Daten im CSV-Format hoch, indem Sie auf den "Durchsuchen" -Button klicken und die Datei auswählen.

2. Wählen Sie die Zeichenkodierung, das Trennzeichen und das Dezimaltrennzeichen entsprechend Ihrer Daten aus. Dies stellt sicher, dass die Daten ordnungsgemäß interpretiert werden.

3. Geben Sie den Durchschnittsabstand zwischen den Messungen in Metern ein. Dieser Wert wird verwendet, um fehlende Daten zu interpolieren und eine gleichmäßige Heatmap-Darstellung zu erzeugen.

4. Wenn Ihre Daten Lücken oder fehlende Werte enthalten, können Sie die Option "Leere Felder interpolieren" aktivieren. Dadurch wird die Heatmap glatter und dichter.

5. Wählen Sie die gewünschte Farbskala aus der Dropdown-Liste oder definieren Sie Ihre benutzerdefinierte Farbskala. Die Farbskala beeinflusst die visuelle Darstellung der Betonüberdeckung in der Heatmap.

6. Klicken Sie auf die Schaltfläche "Heatmap generieren", um die Heatmap zu erstellen. Die generierte Heatmap wird im Anschluss angezeigt.

7. Wenn Sie mit der Heatmap zufrieden sind, können Sie auf die Schaltfläche "Heatmap herunterladen" klicken, um die Heatmap als PNG-Datei auf Ihrem Gerät zu speichern.


