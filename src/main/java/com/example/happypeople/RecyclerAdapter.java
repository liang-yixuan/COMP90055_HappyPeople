package com.example.happypeople;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;

public class RecyclerAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private Context mContext;
    private ArrayList<String> mData;

    public RecyclerAdapter(Context context, ArrayList<String> data) {
        this.mContext = context;
        this.mData = data;
    }

    @NonNull
    @NotNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull @NotNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(mContext).inflate(R.layout.item_layout, parent, false);
        return new NormalHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull @NotNull RecyclerView.ViewHolder holder, int position) {
        NormalHolder normalHolder = (NormalHolder) holder;
        normalHolder.mTv.setText(this.mData.get(position));
    }

    @Override
    public int getItemCount() {
        return this.mData.size();
    }

    public class NormalHolder extends RecyclerView.ViewHolder {

        public TextView mTv;

        public NormalHolder(@NonNull @NotNull View itemView) {
            super(itemView);

            mTv = itemView.findViewById(R.id.item_tv);

        }
    }
}
