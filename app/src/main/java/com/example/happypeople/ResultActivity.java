package com.example.happypeople;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ResultActivity extends AppCompatActivity {

//    private String url = "http://" + "10.0.2.2" + ":" + 5000 + "/";
    private String url = "http://115.146.94.146:5001/";
    private ImageView mIv;
    private RecyclerView mRv;
    private Button mBtn_1;
    private String fileUUID;

    @Override
    protected void onCreate(@Nullable @org.jetbrains.annotations.Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        this.mIv = findViewById(R.id.iv);
        this.mRv = findViewById(R.id.rv);
        this.mBtn_1 = findViewById(R.id.btn_1);

        mBtn_1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(ResultActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });


        Uri selectedImageUri = getIntent().getParcelableExtra("imageURI");
        try {
            String imagePath = getRealPathFromURI(selectedImageUri);
            imagePath = BitmapUtil.compressImage(imagePath);
            uploadImage(imagePath, url);
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    private String getRealPathFromURI(Uri contentURI) {
        String result;
        Cursor cursor = null;
        String[] filePathColumn = {MediaStore.Images.Media.DATA};
        try {
            cursor = getContentResolver().query(contentURI, filePathColumn, null, null, null);
        } catch (Throwable e) {
            e.printStackTrace();
        }
        if (cursor == null) {
            result = contentURI.getPath();
        } else {
            cursor.moveToFirst();
            int idx = cursor.getColumnIndex(MediaStore.Images.Media.DATA);
            result = cursor.getString(idx);
            cursor.close();
        }
        return result;
    }


    private void uploadImage(String imgPath, String url) throws IOException {
        File file = new File(imgPath);
        this.fileUUID = UUID.randomUUID().toString();
        Log.d("imagePath", imgPath);

        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(1000, TimeUnit.SECONDS)
                .readTimeout(1000, TimeUnit.SECONDS)
                .build();
        RequestBody image = RequestBody.create(file, MediaType.parse("image/*"));
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", fileUUID+".png", image)
                .build();
        Request request = new Request.Builder()
                .post(requestBody)
                .url(url)
                .build();

        Toast.makeText(ResultActivity.this, "Uploading...", Toast.LENGTH_SHORT).show();

        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(ResultActivity.this, "Something wrong:"+e.getMessage(), Toast.LENGTH_LONG).show();
                        e.printStackTrace();
                    }
                });
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                Log.d("message", response.message());
                Log.d("content length", String.valueOf(response.body().contentLength()));
                Log.d("content type", String.valueOf(response.body().contentType()));
                InputStream is = response.body().byteStream();
                Bitmap bitmap = BitmapFactory.decodeStream(is);
                response.body().close();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        mIv.setImageBitmap(bitmap);
                    }
                });
                requestJSON(fileUUID, url + "detections");
            }
        });
    }

    public void requestJSON(String fileUUID, String url) {
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(20, TimeUnit.SECONDS)
                .readTimeout(20, TimeUnit.SECONDS)
                .build();
        Request request = new Request.Builder()
                .url(url)
                .post(RequestBody.create(MediaType.parse("text/plain"), fileUUID))
                .build();
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(ResultActivity.this, "Something wrong:"+e.getMessage(), Toast.LENGTH_LONG).show();
                        e.printStackTrace();
                    }
                });
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                try {
                    JSONObject json = new JSONObject(response.body().string());
                    JSONArray obj_array = new JSONArray(json.getString("response"));
                    ArrayList<String> data = new ArrayList<>();
                    for (int i = 0; i < obj_array.length(); i++) {
                        JSONObject obj = obj_array.getJSONObject(i);
                        String result = "Person:    " + obj.getInt("object") + "\n";
                        if (obj.has("age_class_label")) {
                            result = result + "Age:     " + obj.getString("age_class_label") + "\n";
                        } else {
                            result = result + "Age:     Unknown\n";
                        }
                        if (obj.has("gender_class_label")) {
                            result = result + "Gender:  " + obj.getString("gender_class_label") + "\n";
                        } else {
                            result = result + "Gender:  Unknown\n";
                        }
                        if (obj.has("ethnicity_class_label")) {
                            result = result + "Ethnicity: " + obj.getString("ethnicity_class_label") + "\n";
                        } else {
                            result = result + "Ethnicity: Unknown\n";
                        }
                        if (obj.has("emo_class_label")) {
                            result = result + "Emotion: " + obj.getString("emo_class_label");
                        } else {
                            result = result + "Emotion: Unknown";
                        }
                        data.add(result);
                    }
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            if (data.isEmpty()) {
                                Toast.makeText(ResultActivity.this, "No object was detected:(", Toast.LENGTH_LONG).show();
                            }
                            LinearLayoutManager linearLayoutManager = new LinearLayoutManager(ResultActivity.this);
                            linearLayoutManager.setOrientation(RecyclerView.VERTICAL);

                            mRv.setLayoutManager(linearLayoutManager);

                            RecyclerAdapter adapter = new RecyclerAdapter(ResultActivity.this, data);
                            mRv.setAdapter(adapter);
                        }
                    });

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
