import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription

async def handle_offer(pc, offer):
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return answer

async def main():
    pc = RTCPeerConnection()

    async def on_track(track):
        print("Track received:", track.kind)

    pc.addTransceiver("audio")
    pc.addTransceiver("video")

    @pc.on("track")
    async def on_track_internal(track):
        await on_track(track)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state:", pc.iceConnectionState)

    offer = RTCSessionDescription(
        sdp="...",  # Offer SDP from the remote peer
        type="offer"
    )

    answer = await handle_offer(pc, offer)
    print("Answer SDP:", answer.sdp)

asyncio.run(main())
