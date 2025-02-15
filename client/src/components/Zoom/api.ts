import { MediaHandler } from "./mediaHandler";
import { UIController } from "./uiController";

export let validatedWebhookUrl: string | null = null;
let lastWebhookPayload: unknown;

export class APIHandler {
  static async validateWebhook(webhookUrl: string) {
    const response = await fetch("/api/validate-webhook", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ webhookUrl }),
    });

    const data = await response.json();

    if (data.success) {
      // Store the validated URL for later use
      validatedWebhookUrl = webhookUrl;
    }
  }

  static async sendWebhook(isNewMeeting = true) {
    const webhookUrl = validatedWebhookUrl;
    if (!webhookUrl) {
      return;
    }

    // Always send through our server endpoint
    const response = await fetch("/api/send-webhook", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        webhookUrl,
        isNewMeeting,
        existingPayload: isNewMeeting ? null : lastWebhookPayload,
      }),
    });

    const data = await response.json();

    if (data.success) {
      if (isNewMeeting) {
        // Store the successful payload for future RTMS starts
        lastWebhookPayload = data.sent;
      }
      await this.handleWebhookResponse(data, webhookUrl);
    } else {
      throw new Error(data.error || "Failed to get webhook payload");
    }
  }

  static async handleWebhookResponse(payload: Payload, webhookUrl: string) {
    if (
      payload.success &&
      payload.sent?.payload?.payload?.object?.server_urls
    ) {
      UIController.addSignalingLog("Meeting Start Success", {
        server_urls: payload.sent.payload.payload.object.server_urls,
      });
      await MediaHandler.startMediaStream(
        payload.sent.payload.payload.object.server_urls
      );
    }
  }
}

export type Payload =
  | {
      success: true;
      sent?: { payload?: { payload?: { object?: { server_urls: string } } } };
    }
  | { success: false };
