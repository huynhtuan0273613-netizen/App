package com.sbr.autotyper;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.os.Bundle;
import android.util.Log;
import android.view.accessibility.AccessibilityNodeInfo;
import android.content.ClipData;
import android.content.ClipboardManager;
import java.util.List;

public class AutoTyperService extends AccessibilityService {
    private static final String TAG = "SBRAutoTyper";
    private BroadcastReceiver receiver;
    private Handler handler = new Handler(Looper.getMainLooper());
    private boolean running = false;

    @Override
    public void onCreate() {
        super.onCreate();
        IntentFilter filter = new IntentFilter();
        filter.addAction("com.sbr.autotyper.ACTION_START");
        filter.addAction("com.sbr.autotyper.ACTION_STOP");
        receiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String action = intent.getAction();
                if ("com.sbr.autotyper.ACTION_START".equals(action)) {
                    String payload = intent.getStringExtra("payload");
                    int delay_ms = intent.getIntExtra("delay_ms", 0);
                    boolean delay_enabled = intent.getBooleanExtra("delay_enabled", false);
                    startTyping(payload, delay_enabled ? delay_ms : 0);
                } else if ("com.sbr.autotyper.ACTION_STOP".equals(action)) {
                    stopTyping();
                }
            }
        };
        registerReceiver(receiver, filter);
        Log.d(TAG, "AutoTyperService created and receiver registered");
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
    }

    @Override
    public void onInterrupt() {
        Log.d(TAG, "Service interrupted");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (receiver != null) {
            unregisterReceiver(receiver);
        }
        stopTyping();
        Log.d(TAG, "AutoTyperService destroyed");
    }

    private void startTyping(final String payload, final int delay_ms) {
        if (payload == null || payload.isEmpty()) {
            Log.e(TAG, "Empty payload received");
            return;
        }
        
        final String[] chunks = payload.split("\u241E");
        running = true;
        Log.d(TAG, "Starting auto-typing with " + chunks.length + " chunks, delay: " + delay_ms + "ms");
        
        new Thread(() -> {
            for (int i = 0; i < chunks.length && running; i++) {
                final String text = chunks[i];
                final int index = i;
                
                handler.post(() -> {
                    Log.d(TAG, "Processing chunk " + (index + 1) + "/" + chunks.length);
                    boolean success = trySetText(text);
                    if (!success) {
                        pasteWithClipboard(text);
                    }
                    performSendAction();
                });
                
                if (delay_ms > 0 && i < chunks.length - 1) {
                    try {
                        Thread.sleep(delay_ms);
                    } catch (InterruptedException e) {
                        Log.e(TAG, "Sleep interrupted", e);
                        break;
                    }
                }
            }
            running = false;
            Log.d(TAG, "Auto-typing completed");
        }).start();
    }

    private void stopTyping() {
        running = false;
        Log.d(TAG, "Auto-typing stopped");
    }

    private boolean trySetText(String text) {
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root == null) {
            Log.w(TAG, "No root window available");
            return false;
        }
        
        AccessibilityNodeInfo focused = findFocusedEditText(root);
        if (focused != null && focused.isEditable()) {
            Bundle args = new Bundle();
            args.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text);
            boolean result = focused.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, args);
            if (focused != root) {
                focused.recycle();
            }
            root.recycle();
            Log.d(TAG, "trySetText result: " + result);
            return result;
        }
        
        if (root != null) {
            root.recycle();
        }
        return false;
    }

    private AccessibilityNodeInfo findFocusedEditText(AccessibilityNodeInfo root) {
        if (root == null) return null;
        
        if (root.isFocused() && root.isEditable()) {
            return root;
        }
        
        for (int i = 0; i < root.getChildCount(); i++) {
            AccessibilityNodeInfo child = root.getChild(i);
            if (child != null) {
                AccessibilityNodeInfo result = findFocusedEditText(child);
                if (result != null) {
                    if (result != child) {
                        child.recycle();
                    }
                    return result;
                }
                child.recycle();
            }
        }
        return null;
    }

    private void pasteWithClipboard(String text) {
        try {
            ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            if (clipboard != null) {
                ClipData clip = ClipData.newPlainText("sbr_autotyper", text);
                clipboard.setPrimaryClip(clip);
                Log.d(TAG, "Text copied to clipboard");
                
                AccessibilityNodeInfo root = getRootInActiveWindow();
                if (root != null) {
                    AccessibilityNodeInfo focused = findFocusedEditText(root);
                    if (focused != null) {
                        focused.performAction(AccessibilityNodeInfo.ACTION_PASTE);
                        focused.recycle();
                    }
                    root.recycle();
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error pasting from clipboard", e);
        }
    }

    private void performSendAction() {
        try {
            AccessibilityNodeInfo root = getRootInActiveWindow();
            if (root == null) {
                Log.w(TAG, "No root window for send action");
                return;
            }
            
            List<AccessibilityNodeInfo> sendBtns = root.findAccessibilityNodeInfosByText("Send");
            if (sendBtns == null || sendBtns.isEmpty()) {
                sendBtns = root.findAccessibilityNodeInfosByText("send");
            }
            
            if (sendBtns != null && !sendBtns.isEmpty()) {
                for (AccessibilityNodeInfo btn : sendBtns) {
                    if (btn.isClickable()) {
                        btn.performAction(AccessibilityNodeInfo.ACTION_CLICK);
                        Log.d(TAG, "Send button clicked");
                        btn.recycle();
                        root.recycle();
                        return;
                    }
                    btn.recycle();
                }
            }
            
            root.recycle();
            Log.d(TAG, "No send button found - text inserted without sending");
        } catch (Exception e) {
            Log.e(TAG, "Error performing send action", e);
        }
    }
                          }
              
