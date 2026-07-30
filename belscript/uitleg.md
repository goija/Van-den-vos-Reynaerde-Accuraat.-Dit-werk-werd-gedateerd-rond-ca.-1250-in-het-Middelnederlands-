Om een WebRTC-verbinding daadwerkelijk tot stand te brengen tussen een computer en een mobiele telefoon, ontbreekt er nog één cruciale component: de **signaleringsserver** (het 'belscript').

WebRTC is peer-to-peer, maar de apparaten moeten elkaars IP-adressen en mediacapaciteiten (SDP) eerst uitwisselen voordat ze de directe datatunnel kunnen graven. Voor een naadloze integratie met custom netwerkomgevingen en socket-scripts is een lichtgewicht Python WebSocket-server de meest efficiënte oplossing.

Hier is de architectuur in twee delen: het Python-belscript voor de server, en de JavaScript-uitbreiding voor je eerdere HTML-bestand.

### 1. Het Python Belscript (Signaleringsserver)

Dit script fungeert als de telefooncentrale. Het ontvangt de 'oproep' (Offer) van de computer en stuurt deze door naar de mobiel, en vice versa met het antwoord (Answer) en de netwerkpaden (ICE-candidates).

Zorg dat je de `websockets` library hebt geïnstalleerd (`pip install websockets`).

```python
# signaling_server.py
import asyncio
import websockets
import json

# Houd een lijst bij van alle verbonden apparaten (peers)
connected_clients = set()

async def signaling_server(websocket, path):
    # Voeg het nieuwe apparaat (computer of mobiel) toe
    connected_clients.add(websocket)
    print(f"Nieuw apparaat verbonden. Totaal: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Bericht ontvangen type: {data.get('type')}")
            
            # Broadcast het bericht (Offer, Answer, of ICE) naar het ándere apparaat
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
                    
    except websockets.exceptions.ConnectionClosed:
        print("Verbinding verbroken.")
    finally:
        connected_clients.remove(websocket)
        print(f"Apparaat ontkoppeld. Totaal: {len(connected_clients)}")

# Start de server op alle netwerkinterfaces (0.0.0.0) op poort 8765
start_server = websockets.serve(signaling_server, "0.0.0.0", 8765)

print("Signaleringsserver draait... Wachtend op inkomende WebRTC oproepen.")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

```

### 2. De JavaScript Integratie (Client-zijde)

Voeg deze code toe aan het einde van de `<script>` sectie in het eerdere `index.html` document. Dit script verbindt de browser met de Python-server en regelt het geautomatiseerde 'bellen' en 'opnemen'.

Voeg voor het gemak ook één knop toe aan je HTML in het A/V paneel:
`<button id="callBtn">Bel Apparaat (Verzend Offer)</button>`

```javascript
// --- 7. WEBSOCKET SIGNALERING (HET BELSCRIPT) ---

// Vul hier het IP-adres in van de machine waarop signaling_server.py draait
// Bijv: 'ws://192.168.1.50:8765' (of 'wss://' als je SSL gebruikt)
const ws = new WebSocket('ws://JOUW_SERVER_IP:8765'); 

ws.onopen = () => {
    console.log("Verbonden met de Python signaleringsserver.");
};

ws.onmessage = async (message) => {
    const data = JSON.parse(message.data);

    if (!peerConnection) initWebRTC();

    // 1. Ontvang een oproep (Offer) van een ander apparaat
    if (data.type === 'offer') {
        console.log("Oproep ontvangen, antwoord genereren...");
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        
        // Stuur het antwoord terug
        ws.send(JSON.stringify({ type: 'answer', answer: answer }));
    }

    // 2. Ontvang het antwoord (Answer) op een uitgaande oproep
    if (data.type === 'answer') {
        console.log("Antwoord ontvangen, verbinding opbouwen...");
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
    }

    // 3. Ontvang netwerkpaden (ICE Candidates)
    if (data.type === 'ice-candidate') {
        try {
            await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
        } catch (e) {
            console.error("Fout bij toevoegen ICE candidate", e);
        }
    }
};

// Vang lokale netwerkpaden op en stuur ze naar de server
function verzendIceCandidates() {
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            ws.send(JSON.stringify({
                type: 'ice-candidate',
                candidate: event.candidate
            }));
        }
    };
}

// Uitgaande oproep starten
document.getElementById('callBtn').addEventListener('click', async () => {
    if (!peerConnection) initWebRTC();
    verzendIceCandidates(); // Start luisteren naar netwerkpaden

    // Maak een WebRTC Offer (de daadwerkelijke bel-actie)
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    
    // Verzend de Offer naar de signaleringsserver
    ws.send(JSON.stringify({ type: 'offer', offer: offer }));
    console.log("Oproep verzonden.");
});

```

### 3. Essentiële Netwerkvereisten (Computer ↔ Mobiel)

Wanneer je dit kruislings wilt testen (bijvoorbeeld tussen een desktop en een smartphone in hetzelfde netwerk), zijn er een paar strikte technische regels vanuit de browser:

1. **Beveiligingsrestrictie (HTTPS):** Mobiele browsers (zowel Safari op iOS als Chrome op Android) weigeren categorisch toegang tot de microfoon en camera als de website niet via **HTTPS** (of op `localhost`) wordt geserveerd. Als je dit op een lokaal netwerk draait, moet je ofwel een self-signed certificaat genereren, of poort-forwarding/tunnels (zoals ngrok) gebruiken.
2. **STUN-servers:** Binnen een lokaal wifi-netwerk vinden de apparaten elkaar via lokale IP-adressen. Zodra één apparaat op 4G/5G zit en de andere op wifi, heb je een STUN-server nodig om NAT-firewalls te passeren (deze is al opgenomen in de `config` variabele uit de eerdere code via Google's publieke STUN).
3. **De Call Flow:**
* Open de pagina op de computer.
* Open de pagina op de mobiel.
* Accepteer op beide apparaten de camera/mic permissies.
* Klik op **één** van de apparaten op "Bel Apparaat". Het protocol regelt de rest (Offer -> Server -> Mobiel -> Answer -> Server -> Computer -> Tunnel geopend).
